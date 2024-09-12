import os
import random
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext


TELEGRAM_TOKEN = ''
AUDIO_FOLDER = "/path/to/your/folder/"
IMAGE_FOLDER = "/path/to/your/folder/"
ITEMS_FOLDER = "/path/to/your/folder/"
SOUND_FOLDER = "/path/to/your/folder/"
SOUND_FOLDER_BOCHKA = "/path/to/your/folder/subfolder"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /start command from {update.effective_chat.id}")
    
    subfolders = [f.path for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    
    if subfolders:

        random_subfolder = random.choice(subfolders)
        

        audio_files = [f for f in os.listdir(random_subfolder) if f.endswith('.mp3')]
        
        if audio_files:

            random_audio_file = random.choice(audio_files)
            audio_path = os.path.join(random_subfolder, random_audio_file)
            

            with open(audio_path, 'rb') as audio_file:
              await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file)
            
        else:
            await update.message.reply_text("No audios, sorry ((")
    else:
        await update.message.reply_text("No subfolders, sorry ((")


async def hero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /hero command from {update.effective_chat.id}")
    
    subfolders = [f.path for f in os.scandir(IMAGE_FOLDER) if f.is_dir()]
    
    if subfolders:

        random_subfolder = random.choice(subfolders)
        

        image_files = [f for f in os.listdir(random_subfolder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if image_files:

            random_image_file = random.choice(image_files)
            image_path = os.path.join(random_subfolder, random_image_file)
            

            audio_files = [f for f in os.listdir(random_subfolder) if f.endswith('.mp3')]
            
            if audio_files:

                random_audio_file = random.choice(audio_files)
                audio_path = os.path.join(random_subfolder, random_audio_file)
                

                with open(image_path, 'rb') as image_file:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_file)
                

                with open(audio_path, 'rb') as audio_file:
                    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio_file)
            else:
                await update.message.reply_text("No audios, sorry ((")
        else:
            await update.message.reply_text("No images, sorry ((")
    else:
        await update.message.reply_text("No subfolders, sorry ((")


async def build(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received /build command from {update.effective_chat.id}")


    categories = [f for f in os.listdir(ITEMS_FOLDER) if os.path.isdir(os.path.join(ITEMS_FOLDER, f))]


    if len(categories) != 7:
        await update.message.reply_text("Err0r: Expected 7 categories, but found a different number.")
        return


    if "Boots" not in categories:
        await update.message.reply_text("Err0r: 'Boots' category is missing.")
        return


    selected_categories = ["Boots"]


    remaining_categories = [category for category in categories if category != "Boots"]


    selected_categories.extend(random.sample(remaining_categories, 5))

    media_group = []


    for category in selected_categories:
        category_path = os.path.join(ITEMS_FOLDER, category)
        images_in_category = [f for f in os.listdir(category_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]


        if images_in_category:
            random_image = random.choice(images_in_category)
            image_path = os.path.join(category_path, random_image)
            with open(image_path, 'rb') as image_file:
                media_group.append(InputMediaPhoto(image_file.read()))
        else:
            await update.message.reply_text(f"No images found in category {category}.")
            return


    if media_group:
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group, caption="Random build for you. Good luck!")
    else:
        await update.message.reply_text("No images, sorry (((")
        

async def soundpad(update: Update, context: CallbackContext) -> None:
    audio_files = [f for f in os.listdir(SOUND_FOLDER) if f.endswith('.mp3')]
    
    if not audio_files:
        await update.message.reply_text('No sound, sorry (((')
        return
    
    random_file = random.choice(audio_files)
    random_file_path = os.path.join(SOUND_FOLDER, random_file)
    
    with open(random_file_path, 'rb') as audio:
        await update.message.reply_audio(audio)


async def bochka(update: Update, context: CallbackContext) -> None:

    audio_files = [f for f in os.listdir(SOUND_FOLDER_BOCHKA) if f.endswith('.mp3')]
    
    if not audio_files:
        await update.message.reply_text('No sound, sorry (((')
        return
    
    random_file = random.choice(audio_files)
    random_file_path = os.path.join(SOUND_FOLDER_BOCHKA, random_file)
    

    with open(random_file_path, 'rb') as audio:
        await update.message.reply_audio(audio)
        
        
def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hero", hero))
    application.add_handler(CommandHandler("build", build))
    application.add_handler(CommandHandler("soundpad", soundpad))
    application.add_handler(CommandHandler("bochka", bochka))

    application.run_polling()

if __name__ == '__main__':
    main()