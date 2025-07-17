from datetime import datetime, timedelta

class FilterManager:
    def __init__(self):
        self.tocantins_indicators = [
            "TO", "Tocantins", "Palmas", "Araguaína", "Gurupi", 
            "Nacional", "todos os estados", "Região Norte"
        ]
    
    def apply_filters(self, results, include_tocantins=True, exclude_other_states=False, 
                     national_only=False, opportunity_types=None, deadline_filter="Todos"):
        """Apply all filters to search results"""
        filtered_results = results.copy()
        
        # Regional filters
        if include_tocantins and not national_only:
            filtered_results = [r for r in filtered_results if r.get('tocantins_eligible', False)]
        
        if exclude_other_states:
            filtered_results = [r for r in filtered_results if 
                              self._is_national_or_tocantins(r.get('location', ''))]
        
        if national_only:
            filtered_results = [r for r in filtered_results if 
                              self._is_national_opportunity(r.get('location', ''))]
        
        # Opportunity type filter
        if opportunity_types:
            filtered_results = [r for r in filtered_results if r.get('type') in opportunity_types]
        
        # Deadline filter
        filtered_results = self._apply_deadline_filter(filtered_results, deadline_filter)
        
        return filtered_results
    
    def _is_national_or_tocantins(self, location):
        """Check if opportunity is national or Tocantins-specific"""
        location_lower = location.lower()
        return any(indicator.lower() in location_lower for indicator in 
                  ["nacional", "todos os estados", "região norte", "to", "tocantins"])
    
    def _is_national_opportunity(self, location):
        """Check if opportunity is national"""
        location_lower = location.lower()
        return any(indicator.lower() in location_lower for indicator in 
                  ["nacional", "todos os estados"])
    
    def _apply_deadline_filter(self, results, deadline_filter):
        """Apply deadline filtering"""
        if deadline_filter == "Todos":
            return results
        
        now = datetime.now()
        
        if deadline_filter == "Próximos 7 dias":
            cutoff = now + timedelta(days=7)
        elif deadline_filter == "Próximos 30 dias":
            cutoff = now + timedelta(days=30)
        elif deadline_filter == "Próximos 90 dias":
            cutoff = now + timedelta(days=90)
        else:
            return results
        
        return [r for r in results if r.get('deadline') and r['deadline'] <= cutoff]
    
    def get_eligibility_summary(self, results):
        """Get summary of eligibility for results"""
        total = len(results)
        eligible = len([r for r in results if r.get('tocantins_eligible', False)])
        not_eligible = total - eligible
        
        return {
            'total': total,
            'eligible': eligible,
            'not_eligible': not_eligible,
            'percentage_eligible': (eligible / total * 100) if total > 0 else 0
        }
    
    def categorize_by_type(self, results):
        """Categorize results by opportunity type"""
        categories = {}
        for result in results:
            opp_type = result.get('type', 'Outros')
            if opp_type not in categories:
                categories[opp_type] = []
            categories[opp_type].append(result)
        
        return categories
    
    def sort_results(self, results, sort_by="Relevância", sort_order="Decrescente"):
        """Sort results based on criteria"""
        if sort_by == "Data de Publicação":
            results.sort(key=lambda x: x.get('published_date', datetime.min), 
                        reverse=(sort_order == "Decrescente"))
        elif sort_by == "Prazo":
            results.sort(key=lambda x: x.get('deadline', datetime.max), 
                        reverse=(sort_order == "Decrescente"))
        elif sort_by == "Tipo":
            results.sort(key=lambda x: x.get('type', ''), 
                        reverse=(sort_order == "Decrescente"))
        # Default is relevance (current order)
        
        return results
