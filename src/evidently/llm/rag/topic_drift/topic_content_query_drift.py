import pandas as pd
from dataclasses import dataclass
from typing import Any,Dict,List
from src.evidently.llm.rag.topic_drift.topic_distr import get_topic_distr
from src.evidently.llm.rag.rag_utils.categorical import detect_mismatches
from src.evidently.llm.rag.drift import SimilarityCategoricalFeatureDrift


@dataclass
class TopicContentQueryDrift:
    """
    TopicContentQueryDrift is used to assess if the topic distribution words matches
    between the knowledge content base and user queries. The main idea is to check if the user's 
    queries are within context based on the topic words distribution.

    As such this uses categorical similarity methods such as braun,dice,jaccard,overlap and tanimoto
    coefficients.
    """
    content_docs:List[str]
    query_docs:List[str]
    embedding_model:Any

    def query_topic_distribution(self)->Dict[str,Dict[str,float]]:
        """
        The topic distribution of the queries from the user.
        """
        return get_topic_distr(embedding_model=self.embedding_model,
                               text=self.query_docs)

    def content_topic_distribution(self)->Dict[str,Dict[str,float]]:
        """
        The topic distribution ofcontent documents used in the RAG System.
        """
        return get_topic_distr(embedding_model=self.embedding_model,
                               text=self.content_docs)


    def topic_words_dict(self):
        """
        stores the topic words in a dict format.

        Returns:
            Dict[str,str] : a dict with a topic as the key and topic word as the value.
        """
        content_topic_distr=self.content_topic_distribution()
        content_words_dict={}
        
        query_topic_distr=self.query_topic_distribution()
        query_words_dict={}

        for cont_topic,gen_value in content_topic_distr.items():
        
            for cont_topic_word,_ in gen_value.items():

                content_words_dict[cont_topic]=cont_topic_word

        
        for topic,value in query_topic_distr.items():
        
            for topic_word,_ in value.items():

                query_words_dict[topic]=topic_word
        


    def topic_words_dataframes(self):
        """
        stores the topics from the topic distribution of both the queries
        and content base in a dataframe

        Returns:
            pd.DataFrame : two separate dataframes containing main topic words for content base and queries.
        """
        content_topic_distr=self.content_topic_distribution()
        content_words=[]

        query_topic_distr=self.query_topic_distribution()
        query_words=[]

        for topic in content_topic_distr.values():

            for key in list(topic.keys())[:1]:

                content_words.append(key)

        for topic in query_topic_distr.values():

            for key in list(topic.keys())[:1]:

                query_words.append(key)


        content_df=pd.DataFrame({
            "words":content_words
           
        })

        query_df=pd.DataFrame({
            "words":query_words
        })

        return content_df,query_df

    def detect_mismatching_topics(self):
        """
        Detect for mismatching topic words between the knowledge content base and queries.
        """
        content_df,query_df=self.topic_words_dataframes()

        detect_mismatches(ref_data=content_df,
                          ana_data=query_df,
                          feature="words")


    def topic_word_drift(self):
        """
        The Topic-Word Drift using SimilarityFeatureDrift

        Return:
            SimilarityFeatureDrift : with the content and query topic words.
        """
        content_data,query_data=self.topic_words_dataframes()
        return SimilarityCategoricalFeatureDrift(
            ref_data=content_data,
            analysis_data=query_data
        )

    def dice_coeff(self):
        """
        Computes the dice coefficient between the knowledge base content and queries 
        to check for topic alignment.

        Return:
            float:dice coefficient value.
        """
        return self.topic_word_drift().dice_coeff()

    def braun_coeff(self):
        """
        Computes the braun coefficient between the knowledge base content and queries
        to check for topic alignment.

        Return:
            float: braun coefficient value.
        """
        return self.topic_word_drift().braun_coeff()

    def jaccard_coeff(self):
        """
        Computes the braun coefficient between the knowledge base content and queries
        to check for topic alignment.
        
        Return:
            float: jaccard coefficient value.
        """
        return self.topic_word_drift().jaccard_coeff()

    def overlap_coeff(self):
        """
        Computes the overlap coefficient between the knowledge base content and queries
        to check topic alignment.
        
        Return:
            float: overlap coefficient value.
        """
        return self.topic_word_drift().overlap_coeff()

    def tanimoto_coeff(self):
        """
        Computes the tanimoto coefficient between the knowledge base content and queries
        to check for topic alignment.
        
        Return:
            float: tanimoto coefficient value.
        """
        return self.topic_word_drift().tanimoto_coeff()
