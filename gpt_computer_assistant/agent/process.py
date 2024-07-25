import agentops
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize AgentOps
agentops.init(os.getenv('AGENTOPS_API_KEY'))

try:
    from ..llm import *
    from .assistant import *
    from .chat_history import *
    from ..audio.tts import text_to_speech
    from ..audio.stt import speech_to_text
    from ..audio.record import audio_data
    from ..gui.signal import signal_handler
    from ..utils.db import *
    from ..utils.telemetry import my_tracer, os_name
except ImportError:
    from llm import *
    from agent.assistant import *
    from agent.chat_history import *
    from audio.tts import text_to_speech
    from audio.stt import speech_to_text
    from audio.record import audio_data
    from gui.signal import signal_handler
    from utils.db import *
    from utils.telemetry import my_tracer, os_name

import threading
import traceback
from pygame import mixer
import time

last_ai_response = None
user_id = load_user_id()
os_name_ = os_name()

@agentops.record_function('text_to_speech')
def tts_if_you_can(text:str, not_threaded=False, status_edit=False, bypass_other_settings = False):
    try:
        from ..gpt_computer_assistant import the_main_window
        if (not is_just_text_model_active() and not the_main_window.api_enabled) or bypass_other_settings:
            response_path = text_to_speech(text)
            if status_edit:
                signal_handler.assistant_response_ready.emit()

            def play_audio():
                for each_r in response_path:
                    mixer.init()
                    mixer.music.load(each_r)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        if the_main_window.stop_talking:
                            mixer.music.stop()
                            break                            
                        time.sleep(0.1)
                if status_edit:
                    signal_handler.assistant_response_stopped.emit()
            if not not_threaded:
                playback_thread = threading.Thread(target=play_audio)
                playback_thread.start()
            else:
                play_audio()
    except Exception as e:
        agentops.record_event('tts_error', {'error': str(e)})

@agentops.record_function('process_audio')
def process_audio(take_screenshot=True, take_system_audio=False, dont_save_image=False):
    with my_tracer.start_span("process_audio") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("os_name", os_name_)
        try:
            global audio_data, last_ai_response
            from ..gpt_computer_assistant import the_input_box, the_main_window
            from ..audio.record import audio_data, the_input_box_pre

            transcription = speech_to_text(mic_record_location)
            agentops.record_event('transcription_completed', {'length': len(transcription)})

            if take_system_audio:
                transcription2 = speech_to_text(system_sound_location)
                agentops.record_event('system_audio_transcription_completed', {'length': len(transcription2)})

            llm_input = transcription

            if (the_input_box_pre != "" and not the_input_box_pre.startswith("System:") and the_input_box_pre not in last_ai_response):
                llm_input += the_input_box_pre

            if take_system_audio:
                llm_input += " \n Other of USER: " + transcription2

            if the_input_box.toPlainText().startswith("System:"):
                the_main_window.update_from_thread("Transcription Completed. Running AI...")

            agentops.record_event('llm_input_prepared', {'input_length': len(llm_input)})

            llm_output = assistant(
                llm_input,
                get_chat_message_history().messages,
                get_client(),
                screenshot_path=screenshot_path if take_screenshot else None,
                dont_save_image=dont_save_image,
            )
            agentops.record_event('llm_output_received', {'output_length': len(llm_output)})

            if the_input_box.toPlainText().startswith("System:"):
                the_main_window.update_from_thread("AI Response Completed. Generating Audio...")
            last_ai_response = llm_output

            from ..gpt_computer_assistant import the_main_window
            signal_handler.assistant_response_ready.emit()

            def play_text():
                from ..gpt_computer_assistant import the_input_box, the_main_window
                the_main_window.complated_answer = True
                the_main_window.manuel_stop = True
                while the_main_window.reading_thread or the_main_window.reading_thread_2:
                    time.sleep(0.1)                
                the_main_window.read_part_task()
                if the_main_window.stop_talking:
                    the_main_window.stop_talking = False                
                signal_handler.assistant_response_stopped.emit()

            playback_thread = threading.Thread(target=play_text)
            playback_thread.start()
        except Exception as e:
            print("Error in process_audio", e)
            traceback.print_exc()
            from ..gpt_computer_assistant import the_input_box, the_main_window
            the_main_window.update_from_thread("EXCEPTION: " + str(e))
            tts_if_you_can("Exception occurred. Please check the logs.")
            signal_handler.assistant_response_stopped.emit()
            agentops.record_event('process_audio_error', {'error': str(e)})

@agentops.record_function('process_screenshot')
def process_screenshot():
    with my_tracer.start_span("process_screenshot") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("os_name", os_name_)
        try:
            global last_ai_response
            from ..gpt_computer_assistant import the_input_box, the_main_window
            from ..audio.record import audio_data, the_input_box_pre

            llm_input = "I just take a screenshot. for you to remember. Just say 'Ok.' if the user doesnt want anything before."

            if (the_input_box_pre != "" and not the_input_box_pre.startswith("System:") and the_input_box_pre not in last_ai_response):
                llm_input += the_input_box_pre

            agentops.record_event('screenshot_llm_input_prepared', {'input_length': len(llm_input)})

            if the_input_box.toPlainText().startswith("System:"):
                the_main_window.update_from_thread("Transcription Completed. Running AI...")

            llm_output = assistant(
                llm_input,
                get_chat_message_history().messages,
                get_client(),
                screenshot_path=just_screenshot_path,
                dont_save_image=False,
            )
            agentops.record_event('screenshot_llm_output_received', {'output_length': len(llm_output)})

            last_ai_response = llm_output

            from ..gpt_computer_assistant import the_main_window
            signal_handler.assistant_response_ready.emit()

            def play_text():
                from ..gpt_computer_assistant import the_input_box, the_main_window
                the_main_window.complated_answer = True
                the_main_window.manuel_stop = True
                while the_main_window.reading_thread or the_main_window.reading_thread_2:
                    time.sleep(0.1)                      
                the_main_window.read_part_task()
                if the_main_window.stop_talking:
                    the_main_window.stop_talking = False                
                signal_handler.assistant_response_stopped.emit()

            playback_thread = threading.Thread(target=play_text)
            playback_thread.start()

        except Exception as e:
            print("Error in process_screenshot", e)
            traceback.print_exc()
            from ..gpt_computer_assistant import the_input_box, the_main_window
            the_main_window.update_from_thread("EXCEPTION: " + str(e))
            tts_if_you_can("Exception occurred. Please check the logs.")
            signal_handler.assistant_response_stopped.emit()
            agentops.record_event('process_screenshot_error', {'error': str(e)})

@agentops.record_function('process_text')
def process_text(text, screenshot_path=None):
    with my_tracer.start_span("process_text") as span:
        span.set_attribute("user_id", user_id)
        span.set_attribute("os_name", os_name_)
        try:
            global last_ai_response

            llm_input = text
            agentops.record_event('text_llm_input_prepared', {'input_length': len(llm_input)})

            llm_output = assistant(
                llm_input,
                get_chat_message_history().messages,
                get_client(),
                screenshot_path=screenshot_path,
                dont_save_image=True,
            )
            agentops.record_event('text_llm_output_received', {'output_length': len(llm_output)})

            last_ai_response = llm_output

            from ..gpt_computer_assistant import the_main_window

            model = load_model_settings()
            if llm_settings[model]["provider"] == "ollama":
                the_main_window.set_text_to_input_box(last_ai_response)
                
            signal_handler.assistant_response_ready.emit()

            def play_text():
                from ..gpt_computer_assistant import the_input_box, the_main_window
                the_main_window.complated_answer = True
                the_main_window.manuel_stop = True
                while the_main_window.reading_thread or the_main_window.reading_thread_2:
                    time.sleep(0.1)                      
                the_main_window.read_part_task()
                if the_main_window.stop_talking:
                    the_main_window.stop_talking = False
                signal_handler.assistant_response_stopped.emit()

            playback_thread = threading.Thread(target=play_text)
            playback_thread.start()

        except Exception as e:
            print("Error in process_text", e)
            traceback.print_exc()
            from ..gpt_computer_assistant import the_input_box, the_main_window
            the_main_window.update_from_thread("EXCEPTION: " + str(e))
            tts_if_you_can("Exception occurred. Please check the logs.")
            signal_handler.assistant_response_stopped.emit()
            agentops.record_event('process_text_error', {'error': str(e)})

# End the session when the program exits
import atexit

def end_session():
    agentops.end_session('Success')

atexit.register(end_session)