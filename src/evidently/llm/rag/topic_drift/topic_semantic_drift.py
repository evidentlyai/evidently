import pandas as pd
from dataclasses import dataclass
from typing import Any,Dict,List
from src.evidently.llm.rag.topic_drift.topic_distr import get_topic_distr
from src.evidently.llm.rag.rag_utils.categorical import detect_mismatches
from src.evidently.llm.rag.drift import SimilarityCategoricalFeatureDrift


@dataclass
class TopicSemanticContentDrift:
    """
    TopicSemanticContentDrift is used to assess if the topic distribution words matches
    between the the reference and analysis document. The main idea is to check if the new documents topics matches
    with the previous one based on topic distribution.

    As such this uses categorical similarity methods such as braun,dice,jaccard,overlap and tanimoto
    coefficients.
    """
    ref_content_docs:List[str]
    analysis_content_docs:List[str]
    embedding_model:Any

    def ref_topic_distribution(self)->Dict[str,Dict[str,float]]:
        """
        The topic distribution for the reference content.
        """
        return get_topic_distr(embedding_model=self.embedding_model,
                               text=self.query_docs)

    def analysis_topic_distribution(self)->Dict[str,Dict[str,float]]:
        """
        The topic distribution for the analysis content.
        """
        return get_topic_distr(embedding_model=self.embedding_model,
                               text=self.content_docs)


    def topic_words_dict(self):
        """
        stores the topic words in a dict format.

        Returns:
            Dict[str,str] : a dict with a topic as the key and topic word as the value.
        """
        ref_topic_distr=self.ref_topic_distribution()
        ref_words_dict={}
        
        ana_topic_distr=self.analysis_topic_distribution()
        ana_words_dict={}

        for ref_topic,ref_value in ref_topic_distr.items():
        
            for ref_topic_word,_ in ref_value.items():

                ref_words_dict[ref_topic]=ref_topic_word

        
        for topic,value in ana_topic_distr.items():
        
            for topic_word,_ in value.items():

                ana_words_dict[topic]=topic_word
        


    def topic_words_dataframes(self):
        """
        stores the topics from the topic distribution of the two docs in 
        dataframes.

        Returns:
            pd.DataFrame : two separate dataframes containing main topic words for content base and queries.
        """
        ref_topic_distr=self.ref_topic_distribution()
        ref_words=[]

        ana_topic_distr=self.analysis_topic_distribution()
        ana_words=[]

        for topic in ref_topic_distr.values():

            for key in list(topic.keys())[:1]:

                ref_words.append(key)

        for topic in ana_topic_distr.values():

            for key in list(topic.keys())[:1]:

                ana_words.append(key)


        content_df=pd.DataFrame({
            "words":ref_words
           
        })

        query_df=pd.DataFrame({
            "words":ana_words
        })

        return content_df,query_df

    def detect_mismatching_topics(self):
        """
        Detect for mismatching topic words between the the reference and analysis docs.
        """
        content_df,query_df=self.topic_words_dataframes()

        detect_mismatches(ref_data=content_df,
                          ana_data=query_df,
                          feature="words")


    def topic_word_drift(self):
        """
        The Topic-Content Drift using SimilarityFeatureDrift

        Return:
            SimilarityFeatureDrift : with the reference and analysis docs.
        """
        content_data,query_data=self.topic_words_dataframes()
        return SimilarityCategoricalFeatureDrift(
            ref_data=content_data,
            analysis_data=query_data
        )

    def dice_coeff(self):
        """
        Computes the dice coefficient between the reference and analysis docs
        for topic alignment.

        Return:
            float:dice coefficient value.
        """
        return self.topic_word_drift().dice_coeff()

    def braun_coeff(self):
        """
        Computes the braun coefficient between the reference and analysis docs
        for topic alignment.

        Return:
            float: braun coefficient value.
        """
        return self.topic_word_drift().braun_coeff()

    def jaccard_coeff(self):
        """
        Computes the braun coefficient between the reference and analysis docs
        to check for topic alignment.
        
        Return:
            float: jaccard coefficient value.
        """
        return self.topic_word_drift().jaccard_coeff()

    def overlap_coeff(self):
        """
        Computes the overlap coefficient between the reference and analysis docs
        to check  for topic alignment.
        
        Return:
            float: overlap coefficient value.
        """
        return self.topic_word_drift().overlap_coeff()

    def tanimoto_coeff(self):
        """
        Computes the tanimoto coefficient between the reference and analysis docs to
        check for topic alignment.
        
        Return:
            float: tanimoto coefficient value.
        """
        return self.topic_word_drift().tanimoto_coeff()
