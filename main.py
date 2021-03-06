import keras
import modelCreator
import parseText
import sys
import numpy

from keras.callbacks import ModelCheckpoint

import utils

if __name__ == "__main__":
	args = utils.getArgs(sys.argv[1:])
	print args

	path = args.path
	seq_length = args.seq_length

	vocab, char_to_num, num_to_char = parseText.getInfo(path, args)
	x, y = parseText.createDataset(path, char_to_num, seq_length, args)

	models = [modelCreator.buildModel, modelCreator.buildModelCNN, modelCreator.buildModelBiDir]

	model = models[args.model_type](vocab, x)

	with open(args.save_path + "/model.json", "w") as f:
		f.write(model.to_json())

	c = [ModelCheckpoint(args.save_path + "/weights_model-{epoch:02d}-{loss:.5f}.hdf5", monitor="loss", verbose=1, save_best_only=True, mode="min")]

	model.fit(x, y, batch_size=args.batch_size, epochs=args.epochs, verbose=args.verbose, callbacks=c, shuffle=args.random)

	"""numpy.random.random_integers(0, len(x) -1)"""
	modelCreator.generateText(model, numpy.reshape(x[0], (1, x.shape[1], x.shape[2])), args.gen_length, num_to_char, args)
