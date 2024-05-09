import math

import numpy as np

class conditional_independence():

    def __init__(self):

        # You need to fill the None value with *valid* probabilities
        self.X = {0: 0.3, 1: 0.7}  # P(X=x)
        self.Y = {0: 0.3, 1: 0.7}  # P(Y=y)
        self.C = {0: 0.5, 1: 0.5}  # P(C=c)

        self.X_Y = {
            (0, 0): 0.15,  # These should sum to P(X=0)
            (0, 1): 0.15,
            (1, 0): 0.15,
            (1, 1): 0.55
        } # P(X=x, Y=y)

        # Define P(X, C) and P(Y, C) based on some assumptions of interaction
        self.X_C = {
            (0, 0): 0.18,  # These should sum to P(X=0)
            (0, 1): 0.12,
            (1, 0): 0.32,
            (1, 1): 0.38
        }  #P(X=x, C=y)


        self.Y_C = {
            (0, 0): 0.16,  # These should sum to P(Y=0)
            (0, 1): 0.14,
            (1, 0): 0.34,
            (1, 1): 0.36
        } #P(Y=y, C=c)

        # Assume conditional independence to set P(X, Y, C)
        self.X_Y_C = {
            (0, 0, 0): 0.09,  # P(X=0, C=0) * P(Y=0, C=0) / P(C=0)
            (0, 0, 1): 0.06,
            (0, 1, 0): 0.09,
            (0, 1, 1): 0.06,
            (1, 0, 0): 0.07,
            (1, 0, 1): 0.08,
            (1, 1, 0): 0.25,
            (1, 1, 1): 0.30
        } # P(X=x, Y=y, C=c)

    def is_X_Y_dependent(self):
        """
        return True iff X and Y are dependent
        """
        X = self.X
        Y = self.Y
        X_Y = self.X_Y
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        for x, y in X_Y.keys():
            if X_Y[(x, y)] == X[x] * Y[x]:
                return False
        return True
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def is_X_Y_given_C_independent(self):
        """
        return True iff X_given_C and Y_given_C are independent
        """
        X = self.X
        Y = self.Y
        C = self.C
        X_C = self.X_C
        Y_C = self.Y_C
        X_Y_C = self.X_Y_C
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        for (x, y, c), P_x_y_c in X_Y_C.items():
            P_x_c = X_C.get((x, c), 0)
            P_y_c = Y_C.get((y, c), 0)

            if P_x_y_c != P_x_c * P_y_c:
                return False

        return True
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

def poisson_log_pmf(k, rate):
    """
    k: A discrete instance
    rate: poisson rate parameter (lambda)

    return the log pmf value for instance k given the rate
    """
    log_p = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    log_p = np.log(((rate ** k) * (math.e ** (-rate))) / (math.factorial(k)))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return log_p

def get_poisson_log_likelihoods(samples, rates):
    """
    samples: set of univariate discrete observations
    rates: an iterable of rates to calculate log-likelihood by.

    return: 1d numpy array, where each value represent that log-likelihood value of rates[i]
    """
    likelihoods = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    likelihoods = np.zeros(len(rates))

    for i, rate in enumerate(rates):
        likelihoods[i] = sum(poisson_log_pmf(k, rate) for k in samples)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return likelihoods

def possion_iterative_mle(samples, rates):
    """
    samples: set of univariate discrete observations
    rate: a rate to calculate log-likelihood by.

    return: the rate that maximizes the likelihood 
    """
    rate = 0.0
    likelihoods = get_poisson_log_likelihoods(samples, rates) # might help
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    rate = rates[np.argmax(likelihoods)]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return rate

def possion_analytic_mle(samples):
    """
    samples: set of univariate discrete observations

    return: the rate that maximizes the likelihood
    """
    mean = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    mean = np.mean(samples)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return mean

def normal_pdf(x, mean, std):
    """
    Calculate normal density function for a given x, mean and standard deviation.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean value of the distribution.
    - std:  The standard deviation of the distribution.
 
    Returns the normal distribution pdf according to the given mean and std for the given x.    
    """
    p = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    variance = std ** 2
    normalization_factor = 1 / np.sqrt(2 * np.pi * variance)
    exponent = -((x - mean) ** 2) / (2 * variance)

    p = normalization_factor * (math.e ** exponent)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return p

class NaiveNormalClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which encapsulates the relevant parameters(mean, std) for a class conditional normal distribution.
        The mean and std are computed from a given data set.
        
        Input
        - dataset: The dataset as a 2d numpy array, assuming the class label is the last column
        - class_value : The class to calculate the parameters for.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.data = np.copy(dataset)
        self.class_instances = dataset[dataset[:, -1] == class_value][:, :-1]
        self.mean = np.mean(self.class_instances, axis=0)
        self.std = np.std(self.class_instances, axis=0)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    
    def get_prior(self):
        """
        Returns the prior probability of the class according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        class_instances_count = len(self.class_instances)
        total_instances_count = len(self.data)
        prior = class_instances_count / total_instances_count
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior
    
    def get_instance_likelihood(self, x):
        """
        Returns the likelihood probability of the instance under the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        likelihood = np.prod([normal_pdf(x[i], self.mean[i], self.std[i]) for i in range(len(x))])
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior probability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        prior = self.get_prior()
        likelihood = self.get_instance_likelihood(x)
        posterior = prior * likelihood
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior

class MAPClassifier():
    def __init__(self, ccd0 , ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions. 
        One for class 0 and one for class 1, and will predict an instance
        using the class that outputs the highest posterior probability 
        for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods 
                     for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods 
                     for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    
    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        ccd0_posterior = self.ccd0.get_instance_posterior(x)
        ccd1_posterior = self.ccd1.get_instance_posterior(x)
        pred = 0 if ccd0_posterior > ccd1_posterior else 1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred

def compute_accuracy(test_set, map_classifier):
    """
    Compute the accuracy of a given a test_set using a MAP classifier object.
    
    Input
        - test_set: The test_set for which to compute the accuracy (Numpy array). where the class label is the last column
        - map_classifier : A MAPClassifier object capable of prediciting the class for each instance in the testset.
        
    Ouput
        - Accuracy = #Correctly Classified / test_set size
    """
    acc = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    correctly_classified_count = 0
    test_set_size = len(test_set)

    for instance in test_set:
        actual_class = instance[-1]
        class_prediction = map_classifier.predict(instance[:-1])
        correctly_classified_count += 1 if (class_prediction == actual_class) else 0

    acc = correctly_classified_count / test_set_size
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return acc

def multi_normal_pdf(x, mean, cov):
    """
    Calculate multi variable normal density function for a given x, mean and covarince matrix.
 
    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean vector of the distribution.
    - cov:  The covariance matrix of the distribution.
 
    Returns the normal distribution pdf according to the given mean and var for the given x.    
    """
    pdf = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    dimension = x.size
    covariance_det = np.linalg.det(cov)
    inversed_covariance = np.linalg.inv(cov)
    deviation_vector = x - mean
    exponent_term = -0.5 * np.dot(deviation_vector.T, np.dot(inversed_covariance, deviation_vector))
    normalization_constant = 1.0 / (np.sqrt((2 * np.pi) ** dimension * covariance_det))
    pdf = normalization_constant * np.exp(exponent_term)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return pdf

class MultiNormalClassDistribution():

    def __init__(self, dataset, class_value):
        """
        A class which encapsulate the relevant parameters(mean, cov matrix) for a class conditional multi normal distribution.
        The mean and cov matrix (You can use np.cov for this!) will be computed from a given data set.
        
        Input
        - dataset: The dataset as a numpy array
        - class_value : The class to calculate the parameters for.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.data = np.copy(dataset)
        self.class_instances = dataset[dataset[:, -1] == class_value][:, :-1]
        self.mean = np.mean(self.class_instances, axis=0)
        self.cov = np.cov(self.class_instances.T)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        
    def get_prior(self):
        """
        Returns the prior porbability of the class according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        class_instances_count = len(self.class_instances)
        total_instances_count = len(self.data)
        prior = class_instances_count / total_instances_count
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior
    
    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance under the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        likelihood = multi_normal_pdf(x, self.mean, self.cov)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood
    
    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        prior = self.get_prior()
        likelihood = self.get_instance_likelihood(x)
        posterior = prior * likelihood
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior

class MaxPrior():
    def __init__(self, ccd0 , ccd1):
        """
        A Maximum prior classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest prior probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    
    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        ccd0_prior = self.ccd0.get_prior()
        ccd1_prior = self.ccd1.get_prior()
        pred = 0 if ccd0_prior > ccd1_prior else 1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred

class MaxLikelihood():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum Likelihood classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest likelihood probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    
    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        ccd0_likelihood = np.prod(self.ccd0.get_instance_likelihood(x))
        ccd1_likelihood = np.prod(self.ccd1.get_instance_likelihood(x))
        pred = 0 if ccd0_likelihood > ccd1_likelihood else 1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred

EPSILLON = 1e-6 # if a certain value only occurs in the test set, the probability for that value will be EPSILLON.

class DiscreteNBClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which computes and encapsulate the relevant probabilites for a discrete naive bayes 
        distribution for a specific class. The probabilites are computed with laplace smoothing.
        
        Input
        - dataset: The dataset as a numpy array.
        - class_value: Compute the relevant parameters only for instances from the given class.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.data = np.copy(dataset)
        self.class_instances = dataset[dataset[:, -1] == class_value][:, :-1]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
    
    def get_prior(self):
        """
        Returns the prior porbability of the class 
        according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior
    
    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance under 
        the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood
        
    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance 
        under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior


class MAPClassifier_DNB():
    def __init__(self, ccd0 , ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predict an instance
        by the class that outputs the highest posterior probability for the given instance.
    
        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.
    
        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred

    def compute_accuracy(self, test_set):
        """
        Compute the accuracy of a given a testset using a MAP classifier object.

        Input
            - test_set: The test_set for which to compute the accuracy (Numpy array).
        Ouput
            - Accuracy = #Correctly Classified / #test_set size
        """
        acc = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        pass
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return acc


