class SoundController {
  constructor(audioSelector, redirectUrl = null) {
    this.audio = document.querySelector(audioSelector);
    this.redirectUrl = redirectUrl;
  }

  playSoundAndRedirect() {
    if (this.audio) {
      this.audio.currentTime = 0;
      this.audio.play();

      if (this.redirectUrl) {
        this.audio.onended = () => {
          window.location.href = this.redirectUrl;
        };
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const soundController = new SoundController("#click-sound", "songs.html");

  const button = document.querySelector("#get-started-btn");
  if (button) {
    button.addEventListener("click", () => soundController.playSoundAndRedirect());
  }
});
