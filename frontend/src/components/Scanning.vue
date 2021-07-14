<template>
  <v-card class="camera">
    <video class="feed" v-show="!captured"></video>
    <canvas class="feed" id="canvas" v-show="captured"></canvas>
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
</template>

<script>
import axios from "../axios";
import { mapMutations } from "vuex";
import { fabric } from "fabric";

export default {
  data: function () {
    return {
      player: null,
      streaming: false,
      captured: false,
      videoTagHeight: 0,
      videoTagWidth: 0,
      constraint: {
        video: {
          width: {
            ideal: 1920,
          },
          height: {
            ideal: 1080,
          },
        },
      },
    };
  },
  methods: {
    init: function () {
      if (
        "mediaDevices" in navigator &&
        "getUserMedia" in navigator.mediaDevices
      ) {
        navigator.mediaDevices
          .getUserMedia(this.constraint)
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
            this.$swal("No camera found");
          });
      } else {
        this.$swal("This browser is not supported");
      }
    },

    drawBox: function (center_x, center_y, box_width, box_height, confidence) {
      // drawBox: function (confidence = 12) {
      console.log(center_x, center_y, box_width, box_height, confidence);
      return new fabric.Rect({
        top: center_y,
        left: center_x,
        width: box_width,
        height: box_height,
        fill: "rgba(0,0,0,0)",
        stroke: confidence > 0.7 ? "green" : "yellow",
        strokeWidth: 5,
        originX: "center",
        originY: "center",
        // lockMovementX: true,
        // lockMovementY: true,
        hasControls: true,
      });
    },

    // drawBox: function (confidence = 12) {
    //   console.log(center_x, center_y, box_width, box_height, confidence);
    //   return new fabric.Rect({
    //     top: center_x,
    //     left: center_y,
    //     width: box_width,
    //     height: box_height,
    //     fill: "rgba(0,0,0,0)",
    //     stroke: confidence > 0.7 ? "green" : "yellow",
    //     strokeWidth: 5,
    //     originX: "center",
    //     originY: "center",
    //     lockMovementX: true,
    //     lockMovementY: true,
    //     hasControls: false,
    //   });
    // },

    takePicture: function () {
      var canvas = document.querySelector("canvas");
      if (canvas && this.streaming === true) {
        this.videoTagWidth = document.querySelector("video").offsetWidth;
        this.videoTagHeight = document.querySelector("video").offsetHeight;

        canvas.width = this.videoTagWidth;
        canvas.height = this.videoTagHeight;
        const context = canvas.getContext("2d");
        context.imageSmoothingEnabled = true;
        context.imageSmoothingQuality = "high";
        context.drawImage(
          this.player,
          0,
          0,
          this.videoTagWidth,
          this.videoTagHeight
        );

        this.captured = true;

        const data = canvas.toDataURL("image/png");

        var c = new fabric.Canvas("canvas");

        fabric.Image.fromURL(data, function (img) {
          c.backgroundImage = img;
          c.renderAll();
        });

        var self = this;

        axios.post("/api/v1/items/scan/", data).then((response) => {
          if (response.status == 200 && response.data) {
            var c = new fabric.Canvas("canvas");

            fabric.Image.fromURL(data, function (img) {
              c.backgroundImage = img;
              c.renderAll();
            });

            // for (let item of response.data) {
            //   for (let i = 0; i < item.quantity; i++) this.addItemToOrder(item);
            // }
            // this.$store.commit("TOGGLE_SCAN_DIALOG");
            for (var item of response.data.positions) {
              console.log(item);
              console.log(self.videoTagWidth, self.videoTagHeight);
              c.add(
                self.drawBox(
                  item[1] * self.videoTagWidth,
                  item[2] * self.videoTagHeight,
                  item[3] * self.videoTagWidth,
                  item[4] * self.videoTagHeight,
                  0.99
                )
              );
              c.renderAll();
            }
            c.add(
              new fabric.Rect({
                left: 50,
                top: 150,
                fill: "green",
                width: 30,
                height: 30,
              })
            );
          }

          // var rect = new fabric.Rect({
          //   left: 100,
          //   top: 100,
          //   fill: "red",
          //   width: 20,
          //   height: 20,
          //   lockMovementX: true,
          //   lockMovementY: true,
          //   hasControls: false,
          // });

          // c.add(rect);
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
    width: 100%;
    height: auto;
    margin: 0 auto;
    background: transparent;
  }

  .btn-capture {
    position: absolute;
    bottom: 20px;
    left: calc(50% - 28px);
  }
}
</style>