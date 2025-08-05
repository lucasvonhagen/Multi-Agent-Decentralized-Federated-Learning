import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import Evaluation  #Assuming this is another module in your project



#Class that creates ML model, loads data and starts the training on agents
class Training:

    def __init__(self, clientId, dataset_dir='mnist_data'):
        self.clientId = clientId  # For identifying clients
        self.model = self._build_model()
        self.dataset_dir = dataset_dir
        self.__databool = False
        self.client_dir = f'client_{self.clientId}'
        self._setup_client_directory()
        self._ensure_dataset_available()

    #Sets up a directory for the client to store logs and model files
    def _setup_client_directory(self):
        if not os.path.exists(self.client_dir):
            os.makedirs(self.client_dir)
            print(f"{self.clientId} :Created client directory at {self.client_dir}")

    def _build_model(self):
        model = models.Sequential([
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(128, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        print(f"{self.clientId} : MODEL BUILT.")
        return model

    def _ensure_dataset_available(self):
        #Check if directory exists
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
            print(f"{self.clientId} : Created directory: {self.dataset_dir}")

        #Check if dataset is already available locally
        if not os.path.exists(os.path.join(self.dataset_dir, 'mnist.npz')):
            print(f"{self.clientId} :Dataset not found locally. Downloading...")
            mnist = tf.keras.datasets.mnist
            (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
            np.savez(os.path.join(self.dataset_dir, 'mnist.npz'),
                     train_images=train_images, train_labels=train_labels,
                     test_images=test_images, test_labels=test_labels)
            print(f"{self.clientId} :Dataset downloaded and saved.")
        else:
            print(f"{self.clientId} :Dataset found locally.")

    def _load_local_dataset(self):
        with np.load(os.path.join(self.dataset_dir, 'mnist.npz')) as data:
            train_images = data['train_images']
            train_labels = data['train_labels']
            test_images = data['test_images']
            test_labels = data['test_labels']
        return (train_images, train_labels), (test_images, test_labels)

    def loadData(self, sample_size=200, test_sample_size=500):
        if not self.__databool:
            print(f"{self.clientId} :Loading dataset from local storage...")
            (self.train_images_full, self.train_labels_full), (self.test_images_full, self.test_labels_full) = self._load_local_dataset()

            #Shuffles and selects random data for training and testing
            indices = tf.random.shuffle(tf.range(self.train_images_full.shape[0]))
            self.train_images = tf.gather(self.train_images_full, indices[:sample_size])
            self.train_labels = tf.gather(self.train_labels_full, indices[:sample_size])

            test_indices = tf.random.shuffle(tf.range(self.test_images_full.shape[0]))
            self.test_images = tf.gather(self.test_images_full, test_indices[:test_sample_size])
            self.test_labels = tf.gather(self.test_labels_full, test_indices[:test_sample_size])

            self.train_images = tf.cast(self.train_images, tf.float32) / 255.0
            self.test_images = tf.cast(self.test_images, tf.float32) / 255.0

            print(f"{self.clientId} :Data loaded and processed")
            self.__databool = True
        else:
            print(f"{self.clientId} :Shuffling already loaded data...")
            indices = tf.random.shuffle(tf.range(self.train_images_full.shape[0]))
            self.train_images = tf.gather(self.train_images_full, indices[:sample_size])
            self.train_labels = tf.gather(self.train_labels_full, indices[:sample_size])

            test_indices = tf.random.shuffle(tf.range(self.test_images_full.shape[0]))
            self.test_images = tf.gather(self.test_images_full, test_indices[:test_sample_size])
            self.test_labels = tf.gather(self.test_labels_full, test_indices[:test_sample_size])

            self.train_images = tf.cast(self.train_images, tf.float32) / 255.0
            self.test_images = tf.cast(self.test_images, tf.float32) / 255.0

            print(f"{self.clientId} : Data shuffled.")
        
        return (self.train_images, self.train_labels), (self.test_images, self.test_labels)

    def train(self, epochs=1): 
        print(f"{self.clientId} :Loading data for training...")
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = self.loadData()
        print(f"{self.clientId} :Starting training...")

        #Callback to capture training metrics per epoch
        history = self.model.fit(self.train_images, self.train_labels, epochs=epochs, verbose=0)  #Set verbose=0 to suppress progress bar
        print(f"{self.clientId} : Training completed.")

        #Save training history to a file
        training_log_path = os.path.join(self.client_dir, 'training_log.txt')
        with open(training_log_path, 'a') as f:
            f.write(f"Training Metrics for Client {self.clientId} - New Round\n")
            for epoch in range(epochs):
                loss = history.history['loss'][epoch]
                accuracy = history.history['accuracy'][epoch]
                f.write(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.4f}, Accuracy: {accuracy:.4f}\n")
        print(f"{self.clientId} : Training metrics appended to {training_log_path}")


    def evaluate(self):
        print(f"{self.clientId} :Evaluating model...")
        test_loss, test_accuracy = self.model.evaluate(self.test_images, self.test_labels, verbose=0)  #Set verbose=0 to suppress progress bar
        print(f"{self.clientId} :Test loss: {test_loss}")
        print(f"{self.clientId} :Test accuracy: {test_accuracy}")

        #Save evaluation metrics to a file
        evaluation_log_path = os.path.join(self.client_dir, 'evaluation_log.txt')
        with open(evaluation_log_path, 'a') as f:
            f.write(f"Evaluation Metrics for Client {self.clientId} - New Round\n")
            f.write(f"Test Loss: {test_loss:.4f}\n")
            f.write(f"Test Accuracy: {test_accuracy:.4f}\n")
        #print(f"{self.clientId} : Evaluation metrics appended to {evaluation_log_path}")

        return test_loss, test_accuracy



    def getModel(self):
        return self.model

    def getWeights(self):
        return self.model.get_weights()

    def setWeights(self, weights):
        self.model.set_weights(weights)

    def addWeightsFromModel(self):
        weights = self.model.get_weights()
        Evaluation.collectWeights(weights)