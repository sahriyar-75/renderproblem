import requests
import os
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent

# Replace with your actual bot token
BOT_TOKEN = '7919748663:AAFAHuoY8YHLIaH6hY0j8awp432JPszJj2A'

# Replace with your actual YouTube API key
YOUTUBE_API_KEY = 'AIzaSyC6LCQUj9QPcJ2-enpov_cRrQSKMa6ZKIs'

# Replace with your custom web interface URL
WEB_INTERFACE_URL = 'https://teletube.onrender.com/play'

def handle_inline_query(update, context):
  """Handles inline queries, searches YouTube, and sends video results."""
  query = update.inline_query.query.strip()

  if not query:
    return

  try:
    # Construct the YouTube API search URL (Increase maxResults)
    search_url = f"https://www.googleapis.com/youtube/v3/search?" \
           f"part=snippet&q={query}&key={YOUTUBE_API_KEY}&maxResults=20"

    # Send the API request
    response = requests.get(search_url)
    response.raise_for_status() # Raise an exception for HTTP errors

    # Parse the API response
    data = response.json()
    results = []

    for item in data['items']:
      if item['id']['kind'] == 'youtube#video':
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        thumb_url = item['snippet']['thumbnails']['default']['url']

        # Create the InlineQueryResultArticle for each video
        # Pass video ID as a query parameter in the URL
        results.append(
          InlineQueryResultArticle(
            id=video_id,
            title=video_title,
            input_message_content=InputTextMessageContent(
              f"https://www.youtube.com/watch?v={video_id}"
            ),
            thumb_url=thumb_url,
            url=f"{WEB_INTERFACE_URL}/{video_id}" # Pass video ID to your web interface
          )
        )

    # Send the results back to Telegram (Limit to 50 results)
    context.bot.answer_inline_query(
      update.inline_query.id, results[:50], cache_time=300
    ) # Cache for 5 minutes

  except requests.exceptions.RequestException as e:
    print(f"Error fetching YouTube data: {e}")
    context.bot.answer_inline_query(
      update.inline_query.id,
      [
        InlineQueryResultArticle(
          id="error",
          title="Oops! An error occurred.",
          input_message_content=InputTextMessageContent(
            "Something went wrong. Please try again later."
          ),
        )
      ],
      cache_time=0,
    )


def main():
  """Starts the bot."""
  updater = Updater(BOT_TOKEN, use_context=True)
  dispatcher = updater.dispatcher

  dispatcher.add_handler(InlineQueryHandler(handle_inline_query))

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT env variable or default to 5000
    app.run(host='0.0.0.0', port=port)
