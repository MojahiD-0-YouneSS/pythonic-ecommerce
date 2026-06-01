from probo import (
    TABLE,
    THEAD,
    TBODY,
)
from probo.components.light_tags import (
    Lth,
    Ltd,
    Ltr
)



def get_table_tree(*args,**kwargs):
    
    table = TABLE(data_ssdom_id="table_component")
    table_head = THEAD(
        Ltr(*[
            Lth(theader,data_ssdom_id=f"theader-for-{theader}")
         for theader in args]
    ),)
    
    table_body = TBODY(
        
        *[
            Ltr(
                Ltd(tdata),
                Ltd(tdata_values),
            )
            for tdata,tdata_values in kwargs.items()
        ]
    )
    
    table.add(table_head).add(table_body)
    return table