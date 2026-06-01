from typing import Any
from probo import SECTION, H5, DIV, A, I


def QuickActionsSection(**kwargs):
    """Centralized navigation for adding new catalog items."""
    def _link_mapping(kwargs) -> list[Any]:
        l = len(kwargs)
        
        main_link = lambda k,v : (
                A(I(Class="bi bi-plus-lg me-1"), f"Add {k.capitalize()}", 
                href=f"{v}", Class="btn btn-primary me-2"),
        )
        
        
        secondary_link = lambda k,v : (
                A(I(Class="bi bi-plus-circle me-1"), f"Add {k.capitalize()}", 
                href=f"{v}", Class="btn btn-outline-primary me-2"),
        )
        
        
        
        other_link = lambda k,v : (
                A(I(Class="bi bi-tags me-1"), f"Add {k.capitalize()}", 
                href=f"{v}", Class="btn btn-outline-secondary me-2"),
        )
        
        if l == 1:
            return [main_link(k,v) for k,v in kwargs.items()]
        
        if l == 2:
            is_main = True
            collector = []
            for k,v in kwargs.items():
                if is_main:
                    collector.append(main_link(k,v))
                    is_main = False
                else: 
                    collector.append(secondary_link(k,v))
            
            return collector
        
        if l != 0:
            
            is_main = True
            is_secondary = False
            collector = []
            
            for k,v in kwargs.items():
                if is_main:
                    collector.append(main_link(k,v))
                    is_main = False
                    is_secondary = True
                elif is_secondary:
                    collector.append(secondary_link(k,v))
                    is_secondary = False
                else: 
                    collector.append(other_link(k,v))
            return collector
        return []

    return SECTION(
        H5("Quick Actions", Class="mb-3 text-secondary"),
        DIV(
           * _link_mapping(kwargs),
            Class="d-flex"
        ),
        Class="mt-4 p-4 bg-light rounded border border-dashed"
    )