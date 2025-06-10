import asyncio
from gpiozero import Button
from RPLCD.i2c import CharLCD
import aiohttp

# Initialize LCD (adjust I2C address and port for your setup)
lcd = CharLCD("PCF8574", 0x27, cols=20, rows=4)

# Initialize Button
button = Button(21, hold_time=2)  # GPIO pin 18, with 2-second hold detection


# Global variables
run_counter = 0
message_queue = asyncio.PriorityQueue()  # Priority queue for messages
button_queue = asyncio.Queue()  # Queue to track button presses


async def fetch_messages():
    """Fetch messages from an API periodically and add them to the priority queue."""
    api_url = "https://jsonplaceholder.typicode.com/posts"  # Example API
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        for i, item in enumerate(data[:5]):
                            # Add regular messages with medium priority (e.g., priority=5)
                            await message_queue.put((5, item["title"][:16]))
                    else:
                        # Add an error message with high priority
                        await message_queue.put((1, "API Error"))
        except Exception as e:
            # Add an error message with the highest priority
            await message_queue.put((0, f"Error: {e}"))
        await asyncio.sleep(60)  # Fetch new messages every 60 seconds


async def update_counter():
    """Continuously updates the run counter on the LCD."""
    global run_counter
    while True:
        run_counter += 1
        lcd.clear()
        lcd.write_string(f"Run Count:\n{run_counter}")
        await asyncio.sleep(5)  # Update every second


async def listen_for_button():
    """Asynchronous wrapper for button press detection."""
    while True:
        await asyncio.to_thread(
            button.wait_for_press
        )  # Wait for button press asynchronously

        await button_queue.put("pressed")
        await asyncio.sleep(0)


async def show_message_on_button():
    """Displays messages from the priority queue when the button is pressed."""
    while True:
        await button_queue.get()

        lcd.clear()
        if not message_queue.empty():
            print("button pressed")
            # Get the highest-priority message
            priority, message = await message_queue.get()
            lcd.write_string(message)
            await asyncio.sleep(5)  # Keep the message displayed for 5 seconds
        else:
            lcd.write_string("No messages")
            await asyncio.sleep(5)  # Keep "No messages" displayed for 5 seconds


def clear_message_queue():
    """Clears all messages from the priority queue."""
    global message_queue
    message_queue.queue.clear()  # Clear all messages from the internal queue
    lcd.clear()
    lcd.write_string("Queue Cleared!")
    asyncio.run(asyncio.sleep(10))  # Show the message for 2 seconds


# Set up the long-press handler
button.when_held = clear_message_queue


async def main():
    """Main coroutine to run all tasks."""
    # Create tasks for all concurrent operations
    counter_task = asyncio.create_task(update_counter())
    button_listener_task = asyncio.create_task(listen_for_button())
    button_task = asyncio.create_task(show_message_on_button())
    fetch_task = asyncio.create_task(fetch_messages())
    await asyncio.gather(counter_task, button_task, fetch_task, button_listener_task)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    lcd.clear()
    print("Program exited cleanly.")
