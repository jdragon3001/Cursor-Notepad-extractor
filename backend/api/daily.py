"""Daily activity endpoints for the API."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/daily-activity")
async def get_daily_activity(
    orchestrator,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
) -> Dict[str, Any]:
    """Get daily activity summary."""
    try:
        # Get all data
        sessions = orchestrator.sessions
        messages = orchestrator.messages
        daily_stats = orchestrator._daily_stats
        
        # Parse date range
        if start_date and end_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            # Default to last 90 days
            end = date.today()
            start = end - timedelta(days=90)
        
        # Organize data by date
        daily_data = defaultdict(lambda: {
            'date': None,
            'session_count': 0,
            'message_count': 0,
            'lines_added': 0,
            'lines_removed': 0,
            'session_ids': [],
            'composer_suggested_lines': 0,
            'composer_accepted_lines': 0,
            'tab_suggested_lines': 0,
            'tab_accepted_lines': 0,
            'active_minutes': 0.0
        })
        
        # Process sessions
        for session in sessions:
            session_date = session.created_at.date()
            if start <= session_date <= end:
                daily_data[session_date]['date'] = session_date.isoformat()
                daily_data[session_date]['session_count'] += 1
                daily_data[session_date]['lines_added'] += session.total_lines_added
                daily_data[session_date]['lines_removed'] += session.total_lines_removed
                daily_data[session_date]['session_ids'].append(session.composer_id)
                daily_data[session_date]['active_minutes'] += session.duration_minutes
        
        # Process messages (count messages per day)
        for message in messages:
            message_date = message.created_at.date()
            if start <= message_date <= end:
                if daily_data[message_date]['date'] is None:
                    daily_data[message_date]['date'] = message_date.isoformat()
                daily_data[message_date]['message_count'] += 1
        
        # Process daily stats (composer/tab stats)
        for stat in daily_stats:
            if start <= stat.date <= end:
                if daily_data[stat.date]['date'] is None:
                    daily_data[stat.date]['date'] = stat.date.isoformat()
                daily_data[stat.date]['composer_suggested_lines'] = stat.composer_suggested_lines
                daily_data[stat.date]['composer_accepted_lines'] = stat.composer_accepted_lines
                daily_data[stat.date]['tab_suggested_lines'] = stat.tab_suggested_lines
                daily_data[stat.date]['tab_accepted_lines'] = stat.tab_accepted_lines
        
        # Convert to list and sort by date
        daily_list = []
        current_date = start
        while current_date <= end:
            day_data = daily_data.get(current_date, {
                'date': current_date.isoformat(),
                'session_count': 0,
                'message_count': 0,
                'lines_added': 0,
                'lines_removed': 0,
                'session_ids': [],
                'composer_suggested_lines': 0,
                'composer_accepted_lines': 0,
                'tab_suggested_lines': 0,
                'tab_accepted_lines': 0,
                'active_minutes': 0.0
            })
            
            # Calculate acceptance rates
            composer_rate = 0.0
            if day_data['composer_suggested_lines'] > 0:
                composer_rate = (day_data['composer_accepted_lines'] / day_data['composer_suggested_lines']) * 100
            
            tab_rate = 0.0
            if day_data['tab_suggested_lines'] > 0:
                tab_rate = (day_data['tab_accepted_lines'] / day_data['tab_suggested_lines']) * 100
            
            day_data['composer_acceptance_rate'] = round(composer_rate, 1)
            day_data['tab_acceptance_rate'] = round(tab_rate, 1)
            day_data['has_activity'] = day_data['session_count'] > 0 or day_data['message_count'] > 0
            day_data['active_hours'] = round(day_data['active_minutes'] / 60, 1)
            
            daily_list.append(day_data)
            current_date += timedelta(days=1)
        
        # Calculate summary stats
        total_days_active = sum(1 for d in daily_list if d['has_activity'])
        total_sessions = sum(d['session_count'] for d in daily_list)
        total_messages = sum(d['message_count'] for d in daily_list)
        total_lines_added = sum(d['lines_added'] for d in daily_list)
        total_lines_removed = sum(d['lines_removed'] for d in daily_list)
        
        return {
            'daily_data': daily_list,
            'summary': {
                'start_date': start.isoformat(),
                'end_date': end.isoformat(),
                'total_days': len(daily_list),
                'days_active': total_days_active,
                'total_sessions': total_sessions,
                'total_messages': total_messages,
                'total_lines_added': total_lines_added,
                'total_lines_removed': total_lines_removed,
            }
        }
    except Exception as e:
        logger.error(f"Error getting daily activity: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/daily-activity/{date}")
async def get_daily_detail(orchestrator, date_str: str) -> Dict[str, Any]:
    """Get detailed information for a specific day."""
    try:
        # Parse date
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get all data
        sessions = orchestrator.sessions
        messages = orchestrator.messages
        daily_stats = orchestrator._daily_stats
        
        # Filter sessions for this day
        day_sessions = [s for s in sessions if s.created_at.date() == target_date]
        
        # Filter messages for this day
        day_messages = [m for m in messages if m.created_at.date() == target_date]
        
        # Find daily stats for this day
        day_stat = next((s for s in daily_stats if s.date == target_date), None)
        
        # Build session summaries
        session_summaries = []
        for session in sorted(day_sessions, key=lambda s: s.created_at):
            session_messages = [m for m in day_messages if m.composer_id == session.composer_id]
            session_summaries.append({
                'id': session.composer_id,
                'name': session.name,
                'created_at': session.created_at.isoformat(),
                'duration_minutes': round(session.duration_minutes, 1),
                'message_count': len(session_messages),
                'lines_added': session.total_lines_added,
                'lines_removed': session.total_lines_removed,
            })
        
        # Calculate totals
        total_active_minutes = sum(s.duration_minutes for s in day_sessions)
        
        return {
            'date': target_date.isoformat(),
            'sessions': session_summaries,
            'stats': {
                'session_count': len(day_sessions),
                'message_count': len(day_messages),
                'lines_added': sum(s.total_lines_added for s in day_sessions),
                'lines_removed': sum(s.total_lines_removed for s in day_sessions),
                'active_minutes': round(total_active_minutes, 1),
                'active_hours': round(total_active_minutes / 60, 1),
                'composer_suggested_lines': day_stat.composer_suggested_lines if day_stat else 0,
                'composer_accepted_lines': day_stat.composer_accepted_lines if day_stat else 0,
                'composer_acceptance_rate': round(day_stat.composer_acceptance_rate, 1) if day_stat else 0,
                'tab_suggested_lines': day_stat.tab_suggested_lines if day_stat else 0,
                'tab_accepted_lines': day_stat.tab_accepted_lines if day_stat else 0,
                'tab_acceptance_rate': round(day_stat.tab_acceptance_rate, 1) if day_stat else 0,
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        logger.error(f"Error getting daily detail: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

