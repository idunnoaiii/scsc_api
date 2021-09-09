<template>
  <v-layout>
    <v-col lg="8">
      <v-card
        outline
        class="d-flex flex-column justify-space-around"
        height="100%"
      >
        <v-card class="camera">
          <video
            ref="video"
            class="feed"
            id="video"
            autoplay="true"
            playsinline="true"
          ></video>
          <canvas class="feed d-none" id="canvas"></canvas>
        </v-card>
        <h1>{{classes}}</h1>
        <button id="start" @click="start">Start</button>
        <button id="toggle" @click="stop">stop</button>
      </v-card>
    </v-col>
    <v-col lg="4">
      <v-card outline height="100%">
        <v-data-table
          :headers="headers"
          :items="orderItems"
          class="elevation-4"
        >
          <template v-slot:[`item.quantity`]="props">
            <v-edit-dialog>
              {{ props.item.quantity }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.quantity"
                  @change="
                    updateItemQuantity({
                      quantity: props.item.quantity,
                      itemId: props.item.id,
                    })
                  "
                  label="Edit"
                  single-line
                  counter
                  min="1"
                  type="number"
                  step="1"
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon
              small
              color="green darken-1"
              class="mr-2"
              @click="increaseQuantity(item.id)"
            >
              mdi-arrow-up-drop-circle-outline
            </v-icon>
            <v-icon
              small
              color="orange darken-1"
              class="mr-2"
              @click="decreaseQuantity(item.id)"
            >
              mdi-arrow-down-drop-circle-outline
            </v-icon>
            <v-icon small color="red darken-1" @click="deleteItem(item.id)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-layout>
</template>

<script>
var pc = null;
var dc = null;

export default {

  data: function(){
    return {
      toggle: false,
      classes: []
    }
  },

  methods: {
    
    createPeerConnection: function () {
      // var config = {
      //   iceServers : [{urls: ['stun:stun.l.google.com:19302']}]
      // };

      // if (document.getElementById("use-stun").checked) {
      //   config.iceServers = [{ urls: ["stun:stun.l.google.com:19302"] }];
      // }

      pc = new RTCPeerConnection();

      // register some listeners to help debugging
      pc.addEventListener(
        "icegatheringstatechange",
        function () {
          console.log("icegatheringstatechange -> ", pc.iceGatheringState);
        },
        false
      );
      console.log("icegatheringstatechange -> ", pc.iceGatheringState);

      pc.addEventListener(
        "iceconnectionstatechange",
        function () {
          console.log("iceconnectionstatechange -> ", pc.iceConnectionState);
        },
        false
      );
      console.log("iceconnectionstatechange -> ", pc.iceConnectionState);

      pc.addEventListener(
        "signalingstatechange",
        function () {
          console.log("signalingstatechange -> ", pc.signalingState);
        },
        false
      );
      console.log("signalingstatechange -> ", pc.signalingState);

      // connect audio / video
      pc.addEventListener("track", function (evt) {
        if (evt.track.kind == "video")
          document.getElementById("video").srcObject = evt.streams[0];
      });

      return pc;
    },

    negotiate: function () {
      return pc
        .createOffer()
        .then(function (offer) {
          return pc.setLocalDescription(offer);
        })
        .then(function () {
          // wait for ICE gathering to complete
          return new Promise(function (resolve) {
            if (pc.iceGatheringState === "complete") {
              resolve();
            } else {
              let checkState = function () {
                if (pc.iceGatheringState === "complete") {
                  pc.removeEventListener("icegatheringstatechange", checkState);
                  resolve();
                }
              };
              pc.addEventListener("icegatheringstatechange", checkState);
            }
          });
        })
        .then(function () {
          var offer = pc.localDescription;
          // var codec;

          // codec = document.getElementById("video-codec").value;
          // codec = "default";
          // if (codec !== "default") {
          //   offer.sdp = this.sdpFilterCodec("video", codec, offer.sdp);
          // }

          return fetch("http://192.168.1.6:8090/offer_cv", {
            body: JSON.stringify({
              sdp: offer.sdp,
              type: offer.type,
            }),
            headers: {
              "Content-Type": "application/json",
            },
            method: "POST",
          });
        })
        .then(function (response) {
          return response.json();
        })
        .then(function (answer) {
          // document.getElementById("answer-sdp").textContent = answer.sdp;
          return pc.setRemoteDescription(answer);
        })
        .catch(function (e) {
          alert(e);
        });
    },

    start: function () {
      pc = this.createPeerConnection();

      var parameters = { ordered: true };

      dc = pc.createDataChannel("chat", parameters);
  
      dc.onopen= function () {
        dc.send("ping")
      }

      dc.onmessage = function (evt) {
          console.log("channel -> ", " RTT " + evt.data + " ms");
      };

      // pc.ondatachannel = function (evt) {
      //   console.log("ondatachannel -> ", evt.data);
      //   evt.channel.onmessage = function (evt) {
      //     console.log("onmessage -> ", evt.data);
      //   }
      // }

      let self = this;

      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: 1280,
            height: 720,
            frameRate: 4,
          },
        })
        .then(
          function (stream) {
            stream.getTracks().forEach(function (track) {
              pc.addTrack(track, stream);
              console.log(self.toggle)
            });
            return self.negotiate();
          },
          function (err) {
            alert("Could not acquire media: " + err);
          }
        );
    },

    stop: function () {
      // close data channel
      if (dc) {
        dc.close();
      }

      // close transceivers
      if (pc.getTransceivers) {
        pc.getTransceivers().forEach(function (transceiver) {
          if (transceiver.stop) {
            transceiver.stop();
          }
        });
      }

      // close local audio / video
      pc.getSenders().forEach(function (sender) {
        sender.track.stop();
      });

      // close peer connection
      setTimeout(function () {
        pc.close();
      }, 500);
    },
  },

  created() {
    // this.$refs.video
  },
};
</script>


<style lang="scss" scoped>
.camera {
  width: 100vw;

  .feed {
    width: 100%;
    height: auto;
    margin: 0 auto;
    background: transparent;
  }
}
</style>