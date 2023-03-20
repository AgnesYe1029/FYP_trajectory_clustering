import numpy as np
import pandas as pd
from sklearn.cluster import *
import tensorflow as tf
from keras import Input
from encoder import Encoder
from decoder import Decoder
import time
import os

class Traj2Vec:
    def __init__(self, learning_rate, training_epochs, display_step, units, batch_size, frame_dim) -> None:
        # Parameters
        self.learning_rate = learning_rate
        self.training_epochs = training_epochs
        self.display_step = display_step
        # Network Parameters
        # the size of the hidden state for the lstm (notice the lstm uses 2x of this amount so actually lstm will have state of size 2)
        self.units = units
        # 2 different sequences total
        self.batch_size = batch_size
        # the maximum steps for both sequences is 5
        self.max_n_steps = 500
        # each element/frame of the sequence has dimension of 3
        self.frame_dim = frame_dim
        self.encoder = Encoder(self.units, self.batch_size)
        self.decoder = Decoder(self.units, self.batch_size, self.max_n_steps)
        self.optimizer = tf.keras.optimizers.experimental.RMSprop(self.learning_rate)
        self.checkpoint_dir = './training_checkpoints'
        self.checkpoint_prefix = os.path.join(self.checkpoint_dir, "ckpt")
        self.checkpoint = tf.train.Checkpoint(optimizer=self.optimizer,
                                 encoder=self.encoder,
                                 decoder=self.decoder)
        self.traj_vec_dict = dict()

    def loss_function(self, encoder_input, decoder_output, loss_input):
        # Define loss and optimizer, minimize the squared error

        y_true = tf.reshape(encoder_input, [-1])
        y_pred = tf.reshape(decoder_output, [-1])
        loss = 0
        for i in range(len(loss_input)):
            loss += tf.math.reduce_sum(tf.math.square(tf.math.subtract(y_pred[i], y_true[len(loss_input) - i - 1])))
        return loss
    

    def train_step(self, encoder_input_tf, enc_hidden, input_len):
        # print("encoder_input_tf:", encoder_input_tf)
        loss = 0
        loss_input = [tf.reshape(encoder_input_tf[0 : input_len], [-1])]
        encoder_input = [item for item in tf.unstack(encoder_input_tf)]
        decoder_input = [tf.zeros_like(encoder_input_tf[0], name="GO")] + encoder_input_tf
        # print("decoder input", decoder_input)
        
        with tf.GradientTape() as tape:
        
            enc_output, enc_h, enc_c = self.encoder(encoder_input_tf, enc_hidden)

            # Set the AttentionMechanism object with encoder_outputs
            self.decoder.attention_mechanism.setup_memory(enc_output)
            decoder_initial_state = self.decoder.build_initial_state(self.batch_size, [enc_h, enc_c], tf.float32)
            decoder_outputs = self.decoder(decoder_input, decoder_initial_state)
            decoder_output = decoder_outputs.rnn_output

            enc_states_embeddings = [enc_h, enc_c]
                    
            loss = self.loss_function(encoder_input, decoder_output, loss_input)

        variables = self.encoder.trainable_variables + self.decoder.trainable_variables
        # print("variables: ", variables)
        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))
        return loss, enc_states_embeddings

    def traj2vec_model(self, traj):
        self.load_checkpoints()
        self.max_n_steps = max([len(t) for t in traj])

        for epoch in range(self.training_epochs):
            start = time.time()
            trajectoryVecs = []
            enc_hidden = self.encoder.initialize_hidden_state()
            total_loss = 0
            # print(enc_hidden[0].shape, enc_hidden[1].shape)
            for input_data in traj:
            
                input_len = len(input_data)
                defalt = []
                for i in range(0, self.frame_dim):
                    defalt.append(0)
                while len(input_data) < self.max_n_steps:
                    input_data.append(defalt)
                x = np.array(input_data)
                x = x.reshape((self.batch_size, self.max_n_steps, self.frame_dim))
                encoder_input_tf = tf.Variable(x, dtype=tf.float32)

                batch_loss, enc_states_embeddings = self.train_step(encoder_input_tf, enc_hidden, input_len)
                total_loss += batch_loss
                trajectoryVecs.append(enc_states_embeddings)
            if (epoch + 1) % self.display_step == 0:
                self.checkpoint.save(file_prefix = self.checkpoint_prefix)
            
            print('Epoch {} Loss {:.8f}'.format(epoch + 1,total_loss.numpy()))
            print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))
            self.traj_vec_dict = dict(latest_epoch = epoch, latest_trajectoryVecs = trajectoryVecs)
            if epoch == self.training_epochs-1:
                return trajectoryVecs


    def load_checkpoints(self):
        # restoring the latest checkpoint in checkpoint_dir
        try:
            print("checkpoint successfully restored.")
            self.checkpoint.restore(tf.train.latest_checkpoint(self.checkpoint_dir))
        except:
            print("checkpoint NOT restored.")
            pass
