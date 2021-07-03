<template>
  <v-row justify="center">
    <v-dialog
      v-model="$store.state.scanDialog"
      persistent
      max-width="1278px"
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar dark height="48" color="deep-purple">
          <v-btn icon dark @click="$store.commit('TOGGLE_SCAN_DIALOG')">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title><slot name="dialogName"></slot></v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="captured = false"> Clear </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <!-- <v-divider></v-divider> -->
        <v-text-field
          label="Label"
          v-if="$store.state.scanDialog"
          @keyup.enter.native="takePicture"
          class="d-none"
          autofocus
        ></v-text-field>
        <v-card class="camera">
          <video class="feed" autoplay v-show="!captured"></video>
          <canvas class="feed" v-show="captured"></canvas>
          <v-btn
            dark
            class="mx-auto btn-capture"
            color="purple darken-3 d-block"
            fab
            elevation-10
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
import axios from "../axios";
import { mapMutations } from "vuex";

export default {
  data: function () {
    return {
      player: null,
      streaming: false,
      captured: false,
    };
  },
  methods: {
    init: function () {
      if (
        "mediaDevices" in navigator &&
        "getUserMedia" in navigator.mediaDevices
      ) {
        const constraint = {
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
      } else {
        this.$swal("ccc");
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

        this.captured = true;

        const data = canvas.toDataURL("image/png");

        axios.post("/api/v1/items/scan/", data).then((response) => {
          if (response.status == 200 && response.data != []) {
            for (let item of response.data) {
              for (let i = 0; i < item.quantity; i++) this.addItemToOrder(item);
            }
            this.$store.commit("TOGGLE_SCAN_DIALOG");
          }
        });

        // this.player.srcObject.getVideoTracks().forEach(track => track.stop())
      }
    },
    ...mapMutations("POS", {
      addItemToOrder: "ADD_ITEM_TO_ORDER",
    }),
  },

  mounted() {
    console.log("mounted");
    this.init();
  },
};
</script>

<style lang="scss" scoped>
.camera {
  width: 100vw;
  // height: 100vh;
  position: relative;

  .feed {
    display: block;
    width: 100%;
    max-width: 1280px;
    height: 720px;
    margin: 0 auto;
    background-color: black;
  }

  .btn-capture {
    position: absolute;
    bottom: 20px;
    left: calc(50% - 28px);
  }
}
</style>