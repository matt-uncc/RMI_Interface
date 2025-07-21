import sys
import os
# Add parent directory to path to access handler and FRC_ modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handler import handlerDict
from FRC_ import FRC_
import time
import socket



class FRC_methods():
    def __init__(self, s, sequence=1):
        self.handler = handlerDict()
        self.getPackage = FRC_()
        self.s = s
        self.sequence = sequence
        self.curr_x, self.curr_y, self.curr_z, self.curr_w, self.curr_p, self.curr_r = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        self.UtoolNumber = 1
        self.UFrameNumber = 1
        self.sequenceDiff = 0

    # Define the linear move method
    # def linear_move(self, x, y):
    #     motion_package = self.getPackage.LinearMotion(self.sequence,self.UFrameNumber, self.UtoolNumber,  x, y, self.curr_z, self.curr_w, self.curr_p, self.curr_r)
    #     if self.sequenceDiff < 8:
    #         if isinstance(motion_package, dict):
    #             motion_package = self.handler.dict_to_json(motion_package)
    #         # print(f"Sending linear motion package: {motion_package}")
    #         # Send the motion package
    #         self.s.send(motion_package.encode('ascii'))
    #         self.sequence += 1
    #         self.sequenceDiff += 1
    #         return
    #     else:
    #         while self.sequenceDiff >= 8:
    #             # print("sequenceID diff: "+str(self.sequenceDiff))
    #             rcvd = self.s.recv(1096)
    #             if rcvd:
    #                 # print(f"Received raw: {rcvd}")
    #                 errorID, sequenceID = self.recvd_pkg_extract(rcvd)
    #                 if sequenceID is not None:
    #                     self.sequenceDiff = self.sequence - sequenceID
    #                     print(f"Updated sequenceDiff: {self.sequenceDiff}")
    def linear_move(self, x, y, z = None):
    # Prepare the motion package
        if z is None:
            z = self.curr_z
        motion_pkg = self.getPackage.LinearMotion(
            self.sequence, self.UFrameNumber, self.UtoolNumber,
            x, y, z, self.curr_w, self.curr_p, self.curr_r
        )

        # Serialize to JSON if needed
        if isinstance(motion_pkg, dict):
            motion_pkg = self.handler.dict_to_json(motion_pkg)

        # Flow control: send immediately or wait for sequence to catch up
        if self.sequenceDiff < 8:
            try:
                self.s.send(motion_pkg.encode('ascii'))
                self.sequence += 1
                self.sequenceDiff += 1
            except Exception as e:
                print(f"[Error] Failed to send motion package: {e}")
            return

        # Too many outstanding commands – wait for robot to acknowledge some
        print("[Info] Waiting for sequence buffer to drain...")
        while self.sequenceDiff >= 8:
            try:
                rcvd = self.s.recv(4096)
                if not rcvd:
                    print("[Warning] No data received while draining buffer.")
                    continue

                errorID, sequenceID = self.recvd_pkg_extract(rcvd)

                if sequenceID is not None:
                    self.sequenceDiff = self.sequence - sequenceID
                    print(f"[Info] Updated sequenceDiff: {self.sequenceDiff}")
                else:
                    print("[Warning] Received packet without sequenceID.")
            except Exception as e:
                print(f"[Error] Receiving update during buffer wait failed: {e}")
                break

        # After buffer drains, send the motion
        try:
            self.s.send(motion_pkg.encode('ascii'))
            self.sequence += 1
            self.sequenceDiff += 1
        except Exception as e:
            print(f"[Error] Failed to send motion package after wait: {e}")


    # def linear_move(self, x, y):
    #     motion_package = self.getPackage.LinearMotion(
    #         self.sequence, self.UFrameNumber, self.UtoolNumber,
    #         x, y, self.curr_z, self.curr_w, self.curr_p, self.curr_r
    #     )

    #     if isinstance(motion_package, dict):
    #         motion_package = self.handler.dict_to_json(motion_package)

    #     # Wait until buffer has space
    #     while self.sequenceDiff >= 8:
    #         time.sleep(0.1)
    #     self.s.send(motion_package.encode('ascii'))
    #     self.sequence += 1
    #     self.sequenceDiff += 1
        
    def listen(self):
        while True:
            try:
                rcvd = self.s.recv(1024)
                if rcvd:
                    # print(f"Received raw: {rcvd}")
                    errorID, sequenceID = self.recvd_pkg_extract(rcvd)
                    print(f"Received: ErrorID={errorID}, SequenceID={sequenceID}")
                    if sequenceID is not None:
                        self.sequenceDiff = self.sequence - sequenceID
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error in receiver thread: {e}")
                break  # Break loop only on unexpected exceptions


                
            
    
    def recvd_pkg_extract(self, rcvd):
        try:
            if isinstance(rcvd, bytes):
                rcvd = rcvd.decode('ascii')

            # Split all JSON lines
            responses = rcvd.strip().split('\r\n')

            # Filter out empty lines and take the last one
            last_response = ""
            for r in reversed(responses):
                if r.strip():
                    last_response = r.strip()
                    break

            if last_response:
                data = self.handler.json_to_dict(last_response)
                errorID = data.get('ErrorID', None)
                sequenceID = data.get('SequenceID', None)
                print(f"Extracted (last): ErrorID={errorID}, SequenceID={sequenceID}")
                return errorID, sequenceID

        except Exception as e:
            print(f"Error in recvd_pkg_extract: {e}")

        return None, None



    
    def get_current_position(self):
        rcvd = self.send_pkg(self.getPackage.ReadCartesianPosition())
        
        if rcvd is None:
            print("Failed to receive data for current position.")
            return self.curr_x, self.curr_y, self.curr_z, self.curr_w, self.curr_p, self.curr_r

        try:
            if isinstance(rcvd, bytes):
                rcvd = rcvd.decode('ascii')
            pkg = self.handler.json_to_dict(rcvd)
            print(f"Received position package: {pkg}")
            
            if pkg.get('ErrorID', -1) == 0:
                config = pkg.get('Configuration', {})
                self.UtoolNumber = config.get('UToolNumber', 1)
                self.UFrameNumber = config.get('UFrameNumber', 1)
                pos = pkg.get('Position', {})
                self.curr_x = pos.get('X', 0.0)
                self.curr_y = pos.get('Y', 0.0)
                self.curr_z = pos.get('Z', 0.0)
                self.curr_w = pos.get('W', 0.0)
                self.curr_p = pos.get('P', 0.0)
                self.curr_r = pos.get('R', 0.0)
                # print(f"Current Position: X={self.curr_x}, Y={self.curr_y}, Z={self.curr_z}, W={self.curr_w}, P={self.curr_p}, R={self.curr_r}")    
            else:
                print(f"ErrorID not 0, response: {pkg}")
        except Exception as e:
            print(f"Failed to parse position response: {e}")
        
        return self.curr_x, self.curr_y, self.curr_z, self.curr_w, self.curr_p, self.curr_r


    def FRC_initialize(self):
        rcvd = self.send_pkg(self.getPackage.Initialize())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Initialization failed with ErrorID: {errorID}")
        else:
            print("Initialization successful")
        return errorID
    
    def FRC_abort(self):
        rcvd = self.send_pkg(self.getPackage.Abort())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Abort failed with ErrorID: {errorID}")
        else:
            print("Abort successful")
        return errorID
    
    def FRC_pause(self):
        rcvd = self.send_pkg(self.getPackage.Pause())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Pause failed with ErrorID: {errorID}")
        else:
            print("Pause successful")
        return errorID
    
    def FRC_continue(self): 
        rcvd = self.send_pkg(self.getPackage.Continue())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Continue failed with ErrorID: {errorID}")
        else:
            print("Continue successful")
        return errorID
    
    def FRC_get_status(self):
        rcvd = self.send_pkg(self.getPackage.GetStatus())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        self.sequence = pkg.get('NextSequenceID', None)
        if errorID != 0:
            print(f"GetStatus failed with ErrorID: {errorID}")
        else:
            print("GetStatus successful")
            print(f"Next Sequence ID: {self.sequence}")
            print("Error ID:", errorID)
        return errorID

    def FRC_reset(self):
        rcvd = self.send_pkg(self.getPackage.Reset())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Reset failed with ErrorID: {errorID}")
        else:
            print("Reset successful")
        return errorID
    

    def send_pkg(self, pkg, timeout=20):
        try:
            if isinstance(pkg, dict):
                pkg = self.handler.dict_to_json(pkg)

            # print(f"Sending package: {pkg}")
            self.s.send(pkg.encode('ascii'))

            self.s.settimeout(timeout)
            start_time = time.time()

            buffer = b""

            while time.time() - start_time < timeout:
                try:
                    chunk = self.s.recv(1024)
                    if not chunk:
                        break  # Connection closed
                    buffer += chunk

                    # Try to decode and parse
                    decoded = buffer.decode('utf-8', errors='ignore')
                    responses = decoded.strip().split('\r\n')

                    # Filter out empty lines
                    non_empty = [r.strip() for r in responses if r.strip()]
                    if non_empty:
                        last_response = non_empty[-1]
                        print(f"Received raw: {last_response}")
                        return last_response

                except (OSError, TimeoutError) as e:
                    print("Error receiving data:", e)
                    break

        except (OSError, TimeoutError) as e:
            print(f"Send failed: {e}")

        return None

    
    
    
    def FRC_call(self, method_name):
        rcvd = self.send_pkg(self.getPackage.Call(method_name, self.sequence))
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"error calling program: {errorID}")
        else:
            print("executing program")
            self.sequence += 1
        return errorID
    
    def FRC_disconnect(self):
        rcvd = self.send_pkg(self.getPackage.Disconnect())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Disconnect failed with ErrorID: {errorID}")
        else:
            print("Disconnect successful")
        return errorID
    
    def FRC_connect(self):
        rcvd = self.send_pkg(self.getPackage.Connect())
        pkg = self.handler.json_to_dict(rcvd)
        errorID = pkg.get('ErrorID', None)
        if errorID != 0:
            print(f"Connect failed with ErrorID: {errorID}")
        else:
            print("Connect successful")
        return errorID