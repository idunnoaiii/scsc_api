<template>
  <v-card class="camera">
    <video class="feed" v-show="!captured"></video>
    <canvas class="feed" id="canvas" v-show="captured"></canvas>
    <v-container>
      <v-row>
        <v-card
          class="d-flex justify-space-between elevation-0"
          width="100%"
          height="96px"
          color="transparent"
        >
          <v-btn
            dark
            color="orange darken-3 d-inline-block"
            class="align-self-center"
            v-if="hasResponse"
            elevation-10
            @click="cancelResult"
          >
            Cancel</v-btn
          >
          <v-btn
            dark
            class="mx-auto align-self-center"
            color="primary darken-3 d-inline-block"
            v-if="!captured"
            fab
            elevation-10
            @click="takePicture"
          >
            <v-icon>mdi-camera</v-icon></v-btn
          >
          <v-btn
            dark
            color="green darken-3 d-inline-block"
            class="align-self-center"
            v-if="hasResponse"
            elevation-10
            @click="takeMorePicture"
          >
            Continue</v-btn
          >
        </v-card>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import axios from "../axios";
import { mapMutations, mapState } from "vuex";
import { fabric } from "fabric";

export default {
  data: function () {
    return {
      player: null,
      streaming: false,
      captured: false,
      hasResponse: false,
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
      canvas: null,
    };
  },
  computed: {
    ...mapState({
      capturedResponse: "capturedResponse",
    }),
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
      return new fabric.Rect({
        top: center_y,
        left: center_x,
        width: box_width,
        height: box_height,
        fill: "rgba(0,0,0,0)",
        stroke: confidence > 0.8 ? "green" : "yellow",
        strokeWidth: 5,
        originX: "center",
        originY: "center",
        lockMovementX: true,
        lockMovementY: true,
        lockScalingX: true,
        lockScalingY: true,
        lockSkewingX: true,
        lockSkewingY: true,
        // hasControls: false,
      });
    },

    drawText: function (textContent, center_x, center_y) {
      return new fabric.Text(textContent, {
        top: center_y,
        left: center_x,
        originX: "left",
        originY: "top",
        fontSize: 25,
        fontFamily: "roboto",
        fontWeight: "bold",
        strokeWidth: 1,
        stroke: "white",
        fill: "blue",
        hasControls: false,
      });
    },

    cancelResult: function () {
      if (this.canvas) this.canvas.dispose();
      this.captured = false;
      this.hasResponse = false;
      this.$store.commit("SET_CAPTURED_RESPONSE", null);
    },

    takeMorePicture: function () {
      // this.$store.commit("SET_ITEM_DIALOG", true);
      if (this.capturedResponse) {
        for (var pos of this.capturedResponse.positions) {
          if (pos == null) continue;
          let item = this.capturedResponse.items.find((x) => x.id == pos[0]);
          console.log(item.name);
          this.addItemToOrder(item);
        }
        this.$store.commit("SET_CAPTURED_RESPONSE", null);
      }
      if (this.canvas) this.canvas.dispose();
      this.captured = false;
      this.hasResponse = false;
    },

    takePicture: function () {
      var self = this;
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

        const data = canvas.toDataURL("image/png");

        self.captured = true;

        axios
          .post("/api/v1/items/scan/", data)
          .then((response) => {
            self.canvas = new fabric.Canvas("canvas");

            fabric.Image.fromURL(data, function (img) {
              self.canvas.backgroundImage = img;
              self.canvas.renderAll();
            });
            if (response.status == 200 && response.data != null) {
              self.$store.commit("SET_CAPTURED_RESPONSE", response.data);

              // for (let item of response.data) {
              //   for (let i = 0; i < item.quantity; i++) this.addItemToOrder(item);
              // }
              // this.$store.commit("TOGGLE_SCAN_DIALOG");
              let counter = 0;
              for (var pos of response.data.positions) {
                var item = response.data.items.find((x) => x.id == pos[0]);
                var group = new fabric.Group(
                  [
                    self.drawBox(
                      pos[1] * self.videoTagWidth,
                      pos[2] * self.videoTagHeight,
                      pos[3] * self.videoTagWidth,
                      pos[4] * self.videoTagHeight,
                      pos[5]
                    ),
                    self.drawText(
                      item.name + "\n" + item.price + "\n" + counter,
                      (pos[1] - pos[3] / 2) * self.videoTagWidth + 20,
                      (pos[2] - pos[4] / 2) * self.videoTagHeight + 20
                    ),
                  ],
                  {
                    lockMovementX: true,
                    lockMovementY: true,
                    lockScalingX: true,
                    lockScalingY: true,
                    lockSkewingX: true,
                    lockSkewingY: true,
                  }
                );

                group.set("name_", item.name);
                group.set("id_", item.id);
                group.set("index_", counter);
                self.canvas.add(group);
                counter++;
              }
            }

            self.hasResponse = true;

            if (self.canvas) {
              self.canvas.on("mouse:dblclick", function (e) {
                if (e.target && e.target.name_) {
                  self.$store.commit("SET_CAPTURED_ITEM_PICK", {
                    id: e.target.id_,
                    index: e.target.index_,
                    update: function (name, price) {
                      e.target._objects[1].set({ text: `${name}\n${price}` });
                      self.canvas.requestRenderAll();
                      console.log("Updated");
                    },
                  });
                  self.$store.commit("SET_ITEM_DIALOG", true);
                  // e.target._objects[1].set({text: "ahihi"})
                  // self.canvas.requestRenderAll()
                }
              });
            }
          })
          .catch(function () {
            self.captured = false;
            self.hasResponse = false;
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
    let self = this;

    fabric.Object.prototype.transparentCorners = true;
    fabric.Object.prototype.setControlsVisibility({
      tl: false, //top-left
      mt: false, // middle-top
      tr: false, //top-right
      ml: false, //middle-left
      mr: false, //middle-right
      bl: false, // bottom-left
      mb: false, //middle-bottom
      br: false, //bottom-right
      mtr: false,
    });

    var deleteIcon =
      "data:image/svg+xml,%3C%3Fxml version='1.0' encoding='utf-8'%3F%3E%3C!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'%3E%3Csvg version='1.1' id='Ebene_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' width='595.275px' height='595.275px' viewBox='200 215 230 470' xml:space='preserve'%3E%3Ccircle style='fill:%23F44336;' cx='299.76' cy='439.067' r='218.516'/%3E%3Cg%3E%3Crect x='267.162' y='307.978' transform='matrix(0.7071 -0.7071 0.7071 0.7071 -222.6202 340.6915)' style='fill:white;' width='65.545' height='262.18'/%3E%3Crect x='266.988' y='308.153' transform='matrix(0.7071 0.7071 -0.7071 0.7071 398.3889 -83.3116)' style='fill:white;' width='65.544' height='262.179'/%3E%3C/g%3E%3C/svg%3E";
    var img = document.createElement("img");
    img.src = deleteIcon;
    fabric.Object.prototype.controls.deleteControl = new fabric.Control({
      x: 0.5,
      y: -0.5,
      offsetY: 16,
      cursorStyle: "pointer",
      mouseUpHandler: deleteObject,
      render: renderIcon,
      cornerSize: 24,
    });

    function deleteObject(eventData, transform) {
      var target = transform.target;
      console.log("outer_if");
      if (target && target.index_ != undefined) {
        console.log("in_if");
        self.$store.commit("REMOVE_CAPTURED_ITEM", target.index_);
        console.log(target.index_);
      }
      var canvas = target.canvas;
      canvas.remove(target);
      canvas.requestRenderAll();
    }

    function renderIcon(ctx, left, top, styleOverride, fabricObject) {
      var size = this.cornerSize;
      ctx.save();
      ctx.translate(left, top);
      ctx.rotate(fabric.util.degreesToRadians(fabricObject.angle));
      ctx.drawImage(img, -size / 2, -size / 2, size, size);
      ctx.restore();
    }
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