"""
Daily usage statistics calculators (Stats 106-111).

All 6 daily usage stats in a single focused module.
"""

from typing import Dict, Any, List
import logging
import numpy as np
from collections import Counter

from stats.models.daily_stat import DailyStat
from stats.calculators.base_calculator import BaseCalculator

logger = logging.getLogger(__name__)


class DailyUsageCalculator(BaseCalculator):
    """
    Calculate daily usage statistics (Stats 106-111).
    
    Note: Daily stats are only available from Nov 20, 2025 onwards.
    """
    
    def __init__(self, daily_stats: List[DailyStat]):
        """
        Initialize calculator.
        
        Args:
            daily_stats: List of DailyStat objects
        """
        super().__init__(daily_stats)
        self.daily_stats = sorted(daily_stats, key=lambda x: x.date)  # Sort by date
        
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all daily usage stats.
        
        Returns:
            Dictionary of all calculated stats
        """
        logger.info(f"Calculating daily usage stats for {len(self.daily_stats)} days...")
        
        stats = {
            'daily_suggested_lines_composer': self.stat_106_daily_suggested_lines_composer(),
            'daily_accepted_lines_composer': self.stat_107_daily_accepted_lines_composer(),
            'daily_suggested_lines_tab': self.stat_108_daily_suggested_lines_tab(),
            'daily_accepted_lines_tab': self.stat_109_daily_accepted_lines_tab(),
            'daily_acceptance_rate': self.stat_110_daily_acceptance_rate(),
            'composer_vs_tab_usage': self.stat_111_composer_vs_tab_usage(),
        }
        
        logger.info(f"Calculated {len(stats)} daily usage stats")
        return stats
    
    def stat_106_daily_suggested_lines_composer(self) -> Dict[str, Any]:
        """Stat #106: Daily suggested lines (composer)."""
        values = [s.composer_suggested_lines for s in self.daily_stats]
        total = sum(values)
        
        # Get daily breakdown
        daily_breakdown = [
            {'date': s.date.isoformat(), 'lines': s.composer_suggested_lines}
            for s in self.daily_stats
        ]
        
        return self.create_stat_result(
            value=total,
            label='Total composer suggested lines',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='count',
            average_per_day=self.average(values),
            median=self.median(values),
            min=self.min_val(values),
            max=self.max_val(values),
            p95=self.percentile(values, 95),
            days_tracked=len(self.daily_stats),
            daily_breakdown=daily_breakdown[:7]  # Show last 7 days
        )
    
    def stat_107_daily_accepted_lines_composer(self) -> Dict[str, Any]:
        """Stat #107: Daily accepted lines (composer)."""
        values = [s.composer_accepted_lines for s in self.daily_stats]
        total = sum(values)
        
        # Get daily breakdown
        daily_breakdown = [
            {'date': s.date.isoformat(), 'lines': s.composer_accepted_lines}
            for s in self.daily_stats
        ]
        
        return self.create_stat_result(
            value=total,
            label='Total composer accepted lines',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='count',
            average_per_day=self.average(values),
            median=self.median(values),
            min=self.min_val(values),
            max=self.max_val(values),
            p95=self.percentile(values, 95),
            days_tracked=len(self.daily_stats),
            daily_breakdown=daily_breakdown[:7]  # Show last 7 days
        )
    
    def stat_108_daily_suggested_lines_tab(self) -> Dict[str, Any]:
        """Stat #108: Daily suggested lines (tab)."""
        values = [s.tab_suggested_lines for s in self.daily_stats]
        total = sum(values)
        
        return self.create_stat_result(
            value=total,
            label='Total tab suggested lines',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='count',
            average_per_day=self.average(values),
            median=self.median(values),
            days_tracked=len(self.daily_stats)
        )
    
    def stat_109_daily_accepted_lines_tab(self) -> Dict[str, Any]:
        """Stat #109: Daily accepted lines (tab)."""
        values = [s.tab_accepted_lines for s in self.daily_stats]
        total = sum(values)
        
        return self.create_stat_result(
            value=total,
            label='Total tab accepted lines',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='count',
            average_per_day=self.average(values),
            median=self.median(values),
            days_tracked=len(self.daily_stats)
        )
    
    def stat_110_daily_acceptance_rate(self) -> Dict[str, Any]:
        """Stat #110: Daily acceptance rate."""
        # Overall acceptance rate
        total_suggested = sum(s.total_suggested_lines for s in self.daily_stats)
        total_accepted = sum(s.total_accepted_lines for s in self.daily_stats)
        overall_rate = (total_accepted / total_suggested * 100) if total_suggested > 0 else 0
        
        # Composer rate
        composer_suggested = sum(s.composer_suggested_lines for s in self.daily_stats)
        composer_accepted = sum(s.composer_accepted_lines for s in self.daily_stats)
        composer_rate = (composer_accepted / composer_suggested * 100) if composer_suggested > 0 else 0
        
        # Tab rate
        tab_suggested = sum(s.tab_suggested_lines for s in self.daily_stats)
        tab_accepted = sum(s.tab_accepted_lines for s in self.daily_stats)
        tab_rate = (tab_accepted / tab_suggested * 100) if tab_suggested > 0 else 0
        
        # Daily rates for trend analysis
        daily_rates = [
            {
                'date': s.date.isoformat(),
                'rate': s.overall_acceptance_rate,
                'composer_rate': s.composer_acceptance_rate,
                'tab_rate': s.tab_acceptance_rate
            }
            for s in self.daily_stats
        ]
        
        return self.create_stat_result(
            value=overall_rate,
            label='Overall acceptance rate (%)',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='percentage',
            composer_rate=composer_rate,
            tab_rate=tab_rate,
            total_suggested=total_suggested,
            total_accepted=total_accepted,
            daily_rates=daily_rates[:7]  # Show last 7 days
        )
    
    def stat_111_composer_vs_tab_usage(self) -> Dict[str, Any]:
        """Stat #111: Composer vs tab usage comparison."""
        # Total lines
        total_composer = sum(s.composer_suggested_lines for s in self.daily_stats)
        total_tab = sum(s.tab_suggested_lines for s in self.daily_stats)
        total_all = total_composer + total_tab
        
        # Percentages
        composer_pct = (total_composer / total_all * 100) if total_all > 0 else 0
        tab_pct = (total_tab / total_all * 100) if total_all > 0 else 0
        
        # Days with activity
        days_with_composer = len([s for s in self.daily_stats if s.has_composer_activity])
        days_with_tab = len([s for s in self.daily_stats if s.has_tab_activity])
        
        # Average per active day
        composer_values = [s.composer_suggested_lines for s in self.daily_stats if s.has_composer_activity]
        tab_values = [s.tab_suggested_lines for s in self.daily_stats if s.has_tab_activity]
        
        return self.create_stat_result(
            value=total_all,
            label='Total lines suggested (composer + tab)',
            category='Daily Usage',
            data_source='aiCodeTracking.dailyStats',
            stat_type='count',
            composer_lines=total_composer,
            composer_percentage=composer_pct,
            composer_avg_per_active_day=self.average(composer_values) if composer_values else 0,
            days_with_composer=days_with_composer,
            tab_lines=total_tab,
            tab_percentage=tab_pct,
            tab_avg_per_active_day=self.average(tab_values) if tab_values else 0,
            days_with_tab=days_with_tab,
            total_days=len(self.daily_stats)
        )


__all__ = ['DailyUsageCalculator']

