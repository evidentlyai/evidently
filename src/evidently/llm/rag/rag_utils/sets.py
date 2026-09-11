from collections import Counter

def compute_union_values(ref_values,ana_values):
     
     ref_counter_values=Counter(ref_values)
     ana_counter_values=Counter(ana_values)
     union=sum(max(ana_counter_values.get(k,0), ref_counter_values.get(k,0)) for k in set(ana_counter_values + ref_counter_values))


     return union
         
def compute_intersection_values(ref_values,ana_values):
     
     ref_counter_values=Counter(ref_values)
     ana_counter_values=Counter(ana_values)
     intersection=sum(min(ana_counter_values.get(k,0), ref_counter_values.get(k,0)) for k in set(ana_counter_values + ref_counter_values))

     return intersection
