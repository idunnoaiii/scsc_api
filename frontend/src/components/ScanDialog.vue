<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.scanDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark height="48" color="primary">
          <v-btn icon dark @click="$store.commit('TOGGLE_SCAN_DIALOG')">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title><slot name="dialogName"></slot></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="$store.commit('TOGGLE_SCAN_DIALOG')">
              Thoát
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <!-- <v-divider></v-divider> -->
        <v-card class="camera">
          <video class="feed" autoplay></video>
          <canvas class="feed"></canvas>
          <v-btn
            dark
            class="mx-auto"
            color="purple darken-3 d-block"
            fab
            @click="takePicture"
          >
            <v-icon>mdi-camera</v-icon></v-btn
          >
        </v-card>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  data: function () {
    return {
      player: null,
      streaming: false,
    };
  },
  methods: {
    init: function () {
      if (
        "mediaDevices" in navigator &&
        "getUserMedia" in navigator.mediaDevices
      ) {
        let constraint = {
          video: {
            width: {
              min: 640,
              ideal: 1280,
              max: 1920,
            },
            height: {
              min: 360,
              ideal: 720,
              max: 1080,
            },
          },
        };
        navigator.mediaDevices
          .getUserMedia(constraint)
          .then((stream) => {
            this.player = document.querySelector("video");
            if ("srcObject" in this.player) {
              this.player.srcObject = stream;
              this.player.play();
              this.streaming = true;
            }
          })
          .catch(function () {
            this.streaming = false;
          });
      }
    },

    takePicture: function () {
      var canvas = document.querySelector("canvas");
      if (canvas && this.streaming === true) {
        canvas.width = document.querySelector("video").videoWidth;
        canvas.height = document.querySelector("video").videoHeight;
        const context = canvas.getContext("2d");
        context.imageSmoothingEnabled = true;
        context.imageSmoothingQuality = "high";
        context.drawImage(this.player, 0, 0);

        // const imgData = canvas.toDataURL('image/png');
        var data = canvas.toDataURL("image/png");
        console.log(data);
        var request = new XMLHttpRequest();
        request.open("POST", "http://localhost:8000/api/v1/items/scan/");
        request.send(data);

        request.onreadystatechange = function () {
          if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            console.log(request.responseText);
          }
        };

        // this.player.srcObject.getVideoTracks().forEach(track => track.stop())
      }
    },
  },

  beforeUpdate() {
    console.log("mounted");
    this.init();
  },
};
</script>

<style lang="scss" scoped>
.camera {
  width: 100vw;
  height: 100vh;

  .feed {
    display: block;
    width: 100%;
    max-width: 1280px;
    height: 720px;
    margin: 0 auto;
    background-color: black;
  }
}
</style>