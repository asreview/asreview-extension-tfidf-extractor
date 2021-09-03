# Copyright 2019-2021 The ASReview Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sklearn.feature_extraction.text import TfidfVectorizer
import json

from asreview.models.feature_extraction.base import BaseFeatureExtraction


class Tfidf_grab(BaseFeatureExtraction):
    """TF-IDF feature extraction technique.

    Use the standard TF-IDF (Term Frequency-Inverse Document Frequency)
    feature extraction technique from `SKLearn <https://scikit-learn.org/stable/modules/
    generated/sklearn.feature_extraction.text.TfidfVectorizer.html>`__. Gives
    a sparse matrix as output. Works well in combination with
    :class:`asreview.models.NBModel` and other fast training models (given
    that the features vectors are relatively wide).

    Arguments
    ---------
    ngram_max: int
        Can use up to ngrams up to ngram_max. For example in the case of
        ngram_max=2, monograms and bigrams could be used.
    stop_words: str
        When set to 'english', use stopwords. If set to None or 'none',
        do not use stop words.
    """
    name = "tfidf_grab"
    label = "TF-IDF_grab"

    def __init__(self, *args, ngram_max=1, stop_words="english", **kwargs):
        """Initialize tfidf class.
        """
        super().__init__(*args, **kwargs)
        self.ngram_max = ngram_max
        self.stop_words = stop_words
        if stop_words is None or stop_words.lower() == "none":
            sklearn_stop_words = None
        else:
            sklearn_stop_words = self.stop_words
        self._model = TfidfVectorizer(ngram_range=(1, ngram_max),
                                      stop_words=sklearn_stop_words)

    def fit(self, texts):
        self._model.fit(texts)

        with open('vocabulary.json', 'w') as vc:
            json.dump(self._model.vocabulary_, vc,  indent=4)

        self._model.todense()

    def transform(self, texts):
        X = self._model.transform(texts).tocsr()
        return X

