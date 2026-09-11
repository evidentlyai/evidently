from src.evidently.llm.rag.rag_utils.sets import compute_intersection_values,compute_union_values

class SimilarityCategoricalFeatureDrift:

    def __init__(self,ref_data,analysis_data):
        self.ref_data=ref_data
        self.ana_data=analysis_data


    def braun_coeff(self,feature:str): ## Ready for production phase
        intersection=compute_intersection_values(ref_values=self.ref_data[feature],
                                                ana_values=self.ana_data[feature])
            
        N_ref=len(self.ref_data)
        N_ana=len(self.ana_data)
        braun_coeff=intersection/max(N_ref,N_ana)
    
        return braun_coeff
    
    def jaccard_coeff(self,feature:str):  ##Ready for production
        intersection=compute_intersection_values(ref_values=self.ref_data[feature],
                                                 ana_values=self.ana_data[feature]) 
           
        union=compute_union_values(ref_values=self.ref_data[feature],
                                   ana_values=self.ana_data[feature])
        
        jaccard_similarity=intersection/union

        return jaccard_similarity

    def dice_coeff(self,feature:str): ## Ready for production phase
        intersection=compute_intersection_values(ref_values=self.ref_data[feature],
                                                 ana_values=self.ana_data[feature])
      
        N_ref=len(self.ref_data)
        N_ana=len(self.ana_data)

        dice_coeff=2*intersection/(N_ref+ N_ana)
        
        return dice_coeff

    def overlap_coeff(self,feature:str): ## Ready for production phase:
        intersection=compute_intersection_values(ref_values=self.ref_data[feature],
                                                 ana_values=self.ana_data[feature])
        
        N_ref=len(self.ref_data)
        N_ana=len(self.ana_data)
        simpson_coeff=2*intersection/(min(N_ref,N_ana))
        
        return simpson_coeff

    def tanimoto_coeff(self,feature:str): ## Ready for production phase
        intersection=compute_intersection_values(ref_values=self.ref_data[feature],
                                                ana_values=self.ana_data[feature])
            
        tanimoto=intersection/(len(self.ref_data)+ len(self.ana_data)-intersection)
    
        return tanimoto
    
        
