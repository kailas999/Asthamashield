"""
Data collection module for crowdsourced asthma symptom reporting
"""

import json
import csv
import os
from datetime import datetime
from django.conf import settings

class SymptomDataCollector:
    def __init__(self, data_file='symptom_reports.csv'):
        """Initialize the data collector"""
        self.data_file = data_file
        self.headers = [
            'report_id', 'timestamp', 'user_id', 'latitude', 'longitude',
            'wheezing', 'shortness_of_breath', 'chest_tightness', 'coughing',
            'difficulty_sleeping', 'severity', 'verified'
        ]
        self._initialize_file()
    
    def _initialize_file(self):
        """Create the data file with headers if it doesn't exist"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
    
    def save_report(self, report_data):
        """Save a symptom report to the data file"""
        try:
            # Generate report ID
            timestamp = report_data.get('timestamp', datetime.now().isoformat())
            user_id = report_data.get('user_id', 'anonymous')
            report_id = f"rep_{hash(timestamp + user_id) % 1000000}"
            
            # Extract location data
            location = report_data.get('location', {})
            latitude = location.get('latitude', '')
            longitude = location.get('longitude', '')
            
            # Extract symptoms
            symptoms = report_data.get('symptoms', {})
            wheezing = symptoms.get('wheezing', False)
            shortness_of_breath = symptoms.get('shortness_of_breath', False)
            chest_tightness = symptoms.get('chest_tightness', False)
            coughing = symptoms.get('coughing', False)
            difficulty_sleeping = symptoms.get('difficulty_sleeping', False)
            
            # Calculate severity
            severity = self._calculate_severity(symptoms)
            
            # Prepare row data
            row = [
                report_id, timestamp, user_id, latitude, longitude,
                wheezing, shortness_of_breath, chest_tightness, coughing,
                difficulty_sleeping, severity, False  # verified = False initially
            ]
            
            # Append to CSV file
            with open(self.data_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
            
            return report_id
        except Exception as e:
            raise Exception(f"Failed to save report: {str(e)}")
    
    def _calculate_severity(self, symptoms):
        """Calculate severity based on reported symptoms"""
        severity_score = 0
        severity_map = {
            'wheezing': 3,
            'shortness_of_breath': 3,
            'chest_tightness': 2,
            'coughing': 2,
            'difficulty_sleeping': 1
        }
        
        for symptom, present in symptoms.items():
            if present and symptom in severity_map:
                severity_score += severity_map[symptom]
        
        if severity_score >= 5:
            return 'High'
        elif severity_score >= 3:
            return 'Moderate'
        else:
            return 'Low'
    
    def get_reports_by_location(self, latitude, longitude, radius_km=10):
        """Get reports within a certain radius of a location"""
        # This is a simplified implementation
        # In a real system, you would use proper geospatial queries
        reports = []
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Simple distance calculation (not accurate for large distances)
                    try:
                        rep_lat = float(row.get('latitude', 0))
                        rep_lon = float(row.get('longitude', 0))
                        distance = ((rep_lat - latitude) ** 2 + (rep_lon - longitude) ** 2) ** 0.5
                        
                        if distance <= radius_km/100:  # Very rough approximation
                            reports.append(row)
                    except (ValueError, TypeError):
                        continue
            return reports
        except Exception as e:
            raise Exception(f"Failed to retrieve reports: {str(e)}")
    
    def get_reports_by_timeframe(self, start_date, end_date):
        """Get reports within a specific timeframe"""
        reports = []
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        report_time = datetime.fromisoformat(row['timestamp'])
                        if start_date <= report_time <= end_date:
                            reports.append(row)
                    except (ValueError, TypeError):
                        continue
            return reports
        except Exception as e:
            raise Exception(f"Failed to retrieve reports: {str(e)}")
    
    def verify_report(self, report_id):
        """Mark a report as verified"""
        try:
            # Read all data
            rows = []
            with open(self.data_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['report_id'] == report_id:
                        row['verified'] = 'True'
                    rows.append(row)
            
            # Write updated data
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)
                
            return True
        except Exception as e:
            raise Exception(f"Failed to verify report: {str(e)}")

# Global instance
symptom_collector = SymptomDataCollector()

def save_symptom_report(report_data):
    """Convenience function to save a symptom report"""
    return symptom_collector.save_report(report_data)

def get_local_symptom_reports(latitude, longitude, radius_km=10):
    """Convenience function to get local symptom reports"""
    return symptom_collector.get_reports_by_location(latitude, longitude, radius_km)

def get_timeframe_symptom_reports(start_date, end_date):
    """Convenience function to get symptom reports in a timeframe"""
    return symptom_collector.get_reports_by_timeframe(start_date, end_date)