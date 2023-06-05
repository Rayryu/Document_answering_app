css = """
<style>
  .chat-message {
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    display: flex;
  }

  .chat-message.user {
    background-color: #2b313e;
  }

  .chat-message.bot {
    background-color: #475063;
  }

  .chat-message .avatar {
    width: 20%;
  }

  .chat-message .avatar img {
    max-width: 10px;
    max-height: 10px;
    border-radius: 90%;
    object-fit: cover;
  }

  .chat-message .message {
    width: 95%;
    padding: 0 1.5rem;
    color: #fff;
  }
</style>

"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://purepng.com/public/uploads/large/purepng.com-robotrobotprogrammableautomatonelectronics-1701528369303t90mq.png" style="max-height: 90px; max-width: 50px; border-radius: 5%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>

"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://purepng.com/public/uploads/large/purepng.com-user-iconsymbolsiconsapple-iosiosios-8-iconsios-8-721522596134a4bio.png" style="max-height: 90px; max-width: 40px; border-radius: 5%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>

"""
