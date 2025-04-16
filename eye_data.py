class EyeData:
    """
    Class representing eye tracking data parameters from EyeTrackVR OSC messages.
    """
    
    def __init__(self):
        # Initialize all eye parameters with default values
        self._eyes_y = 0.0
        self._left_eye_lid = 0.0
        self._left_eye_lid_expanded_squeeze = 0.0
        self._left_eye_x = 0.0
        self._right_eye_lid = 0.0
        self._right_eye_lid_expanded_squeeze = 0.0
        self._right_eye_x = 0.0
        self._timestamp = None
    
    # Eyes Y getters and setters
    def get_eyes_y(self):
        """Get the vertical position of both eyes"""
        return self._eyes_y
    
    def set_eyes_y(self, value):
        """Set the vertical position of both eyes"""
        self._eyes_y = float(value)
    
    # Left Eye Lid getters and setters
    def get_left_eye_lid(self):
        """Get the left eye lid position"""
        return self._left_eye_lid
    
    def set_left_eye_lid(self, value):
        """Set the left eye lid position"""
        self._left_eye_lid = float(value)
    
    # Left Eye Lid Expanded Squeeze getters and setters
    def get_left_eye_lid_expanded_squeeze(self):
        """Get the left eye lid expanded/squeeze value"""
        return self._left_eye_lid_expanded_squeeze
    
    def set_left_eye_lid_expanded_squeeze(self, value):
        """Set the left eye lid expanded/squeeze value"""
        self._left_eye_lid_expanded_squeeze = float(value)
    
    # Left Eye X getters and setters
    def get_left_eye_x(self):
        """Get the horizontal position of the left eye"""
        return self._left_eye_x
    
    def set_left_eye_x(self, value):
        """Set the horizontal position of the left eye"""
        self._left_eye_x = float(value)
    
    # Right Eye Lid getters and setters
    def get_right_eye_lid(self):
        """Get the right eye lid position"""
        return self._right_eye_lid
    
    def set_right_eye_lid(self, value):
        """Set the right eye lid position"""
        self._right_eye_lid = float(value)
    
    # Right Eye Lid Expanded Squeeze getters and setters
    def get_right_eye_lid_expanded_squeeze(self):
        """Get the right eye lid expanded/squeeze value"""
        return self._right_eye_lid_expanded_squeeze
    
    def set_right_eye_lid_expanded_squeeze(self, value):
        """Set the right eye lid expanded/squeeze value"""
        self._right_eye_lid_expanded_squeeze = float(value)
    
    # Right Eye X getters and setters
    def get_right_eye_x(self):
        """Get the horizontal position of the right eye"""
        return self._right_eye_x
    
    def set_right_eye_x(self, value):
        """Set the horizontal position of the right eye"""
        self._right_eye_x = float(value)
    
    # Timestamp getters and setters
    def get_timestamp(self):
        """Get the timestamp of the eye data"""
        return self._timestamp
    
    def set_timestamp(self, value):
        """Set the timestamp of the eye data"""
        self._timestamp = value
    
    def update_from_osc_message(self, message_dict):
        """
        Update the eye data attributes from a dictionary of OSC messages.
        
        Args:
            message_dict: Dictionary with OSC addresses as keys and parameter values as values
        """
        if '/avatar/parameters/EyesY' in message_dict:
            self.set_eyes_y(message_dict['/avatar/parameters/EyesY'][0])
            
        if '/avatar/parameters/LeftEyeLid' in message_dict:
            self.set_left_eye_lid(message_dict['/avatar/parameters/LeftEyeLid'][0])
            
        if '/avatar/parameters/LeftEyeLidExpandedSqueeze' in message_dict:
            self.set_left_eye_lid_expanded_squeeze(message_dict['/avatar/parameters/LeftEyeLidExpandedSqueeze'][0])
            
        if '/avatar/parameters/LeftEyeX' in message_dict:
            self.set_left_eye_x(message_dict['/avatar/parameters/LeftEyeX'][0])
            
        if '/avatar/parameters/RightEyeLid' in message_dict:
            self.set_right_eye_lid(message_dict['/avatar/parameters/RightEyeLid'][0])
            
        if '/avatar/parameters/RightEyeLidExpandedSqueeze' in message_dict:
            self.set_right_eye_lid_expanded_squeeze(message_dict['/avatar/parameters/RightEyeLidExpandedSqueeze'][0])
            
        if '/avatar/parameters/RightEyeX' in message_dict:
            self.set_right_eye_x(message_dict['/avatar/parameters/RightEyeX'][0])
            
        # Update timestamp
        import datetime
        self.set_timestamp(datetime.datetime.now())
    
    def to_csv_row(self):
        """
        Convert the eye data to a list suitable for CSV writing.
        
        Returns:
            List of values in the order matching the CSV headers
        """
        return [
            self.get_eyes_y(),
            self.get_left_eye_lid(),
            self.get_left_eye_lid_expanded_squeeze(),
            self.get_left_eye_x(),
            self.get_right_eye_lid(),
            self.get_right_eye_lid_expanded_squeeze(),
            self.get_right_eye_x(),
            self.get_timestamp().strftime("%H:%M:%S") if self.get_timestamp() else ""
        ]
    
    def __str__(self):
        """String representation of the eye data"""
        return (f"EyeData(eyes_y={self.get_eyes_y()}, "
                f"left_eye_lid={self.get_left_eye_lid()}, "
                f"left_eye_lid_expanded_squeeze={self.get_left_eye_lid_expanded_squeeze()}, "
                f"left_eye_x={self.get_left_eye_x()}, "
                f"right_eye_lid={self.get_right_eye_lid()}, "
                f"right_eye_lid_expanded_squeeze={self.get_right_eye_lid_expanded_squeeze()}, "
                f"right_eye_x={self.get_right_eye_x()}, "
                f"timestamp={self.get_timestamp()})")
    
    def is_complete(self):
        """
        Check if all required eye tracking parameters have been received.
        
        Returns:
            bool: True if all required parameters are present
        """
        # Check if all essential parameters have been set
        return (self.get_eyes_y() is not None and
                self.get_left_eye_lid() is not None and
                self.get_left_eye_lid_expanded_squeeze() is not None and
                self.get_left_eye_x() is not None and
                self.get_right_eye_lid() is not None and
                self.get_right_eye_lid_expanded_squeeze() is not None and
                self.get_right_eye_x() is not None)