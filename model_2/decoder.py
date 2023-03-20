import tensorflow as tf
import tensorflow_addons as tfa

class Decoder(tf.keras.Model):
  def __init__(self, dec_units, batch_sz, max_length_input, attention_type='luong'):
    super(Decoder, self).__init__()
    self.batch_sz = batch_sz
    self.dec_units = dec_units
    self.attention_type = attention_type
    self.max_length_input = max_length_input

    # Define the fundamental cell for decoder recurrent structure
    self.decoder_rnn_cell = tf.keras.layers.LSTMCell(self.dec_units)



    # Sampler
    self.sampler = tfa.seq2seq.sampler.TrainingSampler()

    # Create attention mechanism with memory = None
    self.attention_mechanism = self.build_attention_mechanism(self.dec_units, 
                                                              None, self.batch_sz*[self.max_length_input], self.attention_type)

    # Wrap attention mechanism with the fundamental rnn cell of decoder
    self.rnn_cell = self.build_rnn_cell(batch_sz)

    # Define the decoder with respect to fundamental rnn cell
    self.decoder = tfa.seq2seq.BasicDecoder(self.rnn_cell, sampler=self.sampler)


  def build_rnn_cell(self, batch_sz):
    rnn_cell = tfa.seq2seq.AttentionWrapper(self.decoder_rnn_cell, 
                                  self.attention_mechanism, attention_layer_size=self.dec_units)
    return rnn_cell

  def build_attention_mechanism(self, dec_units, memory, memory_sequence_length, attention_type='luong'):
    # ------------- #
    # typ: Which sort of attention (Bahdanau, Luong)
    # dec_units: final dimension of attention outputs 
    # memory: encoder hidden states of shape (batch_size, max_length_input, enc_units)
    # memory_sequence_length: 1d array of shape (batch_size) with every element set to max_length_input (for masking purpose)

    if(attention_type=='bahdanau'):
      return tfa.seq2seq.BahdanauAttention(units=dec_units, memory=memory, memory_sequence_length=memory_sequence_length)
    else:
      return tfa.seq2seq.LuongAttention(units=dec_units, memory=memory, memory_sequence_length=memory_sequence_length)


  def build_initial_state(self, batch_sz, encoder_state, Dtype):
    decoder_initial_state = self.rnn_cell.get_initial_state(batch_size=batch_sz, dtype=Dtype)
    decoder_initial_state = decoder_initial_state.clone(cell_state=encoder_state)
    return decoder_initial_state
  

  def call(self, inputs, initial_state):
    x = inputs
    # outputs, _, _ = self.decoder(x, initial_state=initial_state, sequence_length=self.batch_sz*[max_length_output-1])
    outputs, _, _ = self.decoder(x, initial_state=initial_state)
    return outputs

# class Decoder(tf.keras.Model):
#   def __init__(self, dec_units, batch_sz, frame_dim):
#     super(Decoder, self).__init__()
#     self.batch_sz = batch_sz
#     self.dec_units = dec_units # pass in the size
#     self.frame_dim = frame_dim

#     # Define the fundamental cell for decoder recurrent structure
#     self.decoder_rnn_cell = tf.keras.layers.LSTMCell(self.dec_units)


#     # Sampler
#     self.sampler = tfa.seq2seq.sampler.TrainingSampler()


#     # Define the decoder with respect to fundamental rnn cell
#     self.decoder = tfa.seq2seq.BasicDecoder(self.decoder_rnn_cell, sampler=self.sampler)


#   def build_initial_state(self, batch_sz, encoder_state, Dtype):
#     decoder_initial_state = self.decoder_rnn_cell.get_initial_state(batch_size=batch_sz, dtype=Dtype)
#     return decoder_initial_state


#   def call(self, inputs, initial_state):
#     x = inputs
#     # input_lengths = tf.fill([self.batch_sz, self.frame_dim], max_n_steps)
#     # outputs, _, _ = self.decoder(x, initial_state=initial_state, sequence_length=input_lengths)
#     outputs, _, _ = self.decoder(x, initial_state=initial_state)
#     return outputs