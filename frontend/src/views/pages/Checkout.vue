<template>
  <v-layout>
    <v-col lg="8">
      <v-card
        outline
        class="d-flex flex-column justify-md-space-between"
        height="100%"
      >
        <v-card color="primary" flat tile>
          <v-toolbar dark color="primary">
            <v-toolbar-title>SCSC</v-toolbar-title>

            <v-spacer></v-spacer>

            <span class="text-h5">{{ user.full_name }}</span>
            <v-btn icon>
              <v-icon>mdi-account </v-icon>
            </v-btn>
          </v-toolbar>
        </v-card>
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
        <!-- <h1>{{ classes }}</h1> -->
        <div class="d-flex justify-lg-space-around pa-6">
          <v-btn x-large dark id="toggle" color="orange" @click="stopMedia">
            <v-icon dark class="mx-0" color="white"> mdi-cancel </v-icon>
            EXIT
          </v-btn>
          <v-btn x-large dark color="green" id="start" @click="checkout">
            <v-icon dark class="mx-0" color="white"> mdi-cash </v-icon>
            CHECKOUT
          </v-btn>
          <v-btn x-large dark color="green" @click="login_chuoi">
            <v-icon dark class="mx-0" color="white"> mdi-cash </v-icon>
            LOGIN
          </v-btn>
        </div>
      </v-card>
    </v-col>
    <v-col lg="4">
      <v-card outline height="100%" tile class="d-flex flex-column">
        <v-card-title
          style="background-color: #1976d2"
          class="white--text"
          height="48px"
        >
          <div class="text-h5">Details</div>
        </v-card-title>
        <v-card-text
          style="max-height: calc(100% - 200px);height: calc(100% - 200px);}"
        >
          <v-simple-table fixed-header style="height: calc(100% - 120px)">
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Price</th>
                  <th class="text-left">Quantity</th>
                  <th class="text-left">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in orderItems" :key="item.name">
                  <td>{{ item.name }}</td>
                  <td>{{ item.price }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>{{ item.price * item.quantity }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>
        <v-card-actions class="d-flex-row">
          <div class="text-h5 d-inline-flex px-5">Total Price:</div>
          <div class="text-h5 d-inline-flex px-5">{{ totalPrice }}</div>
        </v-card-actions>
        <v-card-actions class="d-flex-row">
          <div class="text-h5 d-inline-flex px-5">Balance:</div>
          <div class="text-h5 d-inline-flex px-5">{{ user.balance }}</div>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-dialog
      v-model="scanScreen"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      persistent
    >
      <v-card>
        <v-container id="login" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="10">
              <v-card
                class="elevation-12 rounded-xl"
                style="background-color: rgb(25 118 210 / 81%)"
              >
                <v-card-title class="justify-center">
                  <div class="text-center my-10">
                    <div class="text-h3 white--text">SCSC Welcome</div>
                    <!-- <div class="text-h6">Scan QRCode to Login</div> -->
                  </div>
                </v-card-title>
                <v-card-text>
                  <v-container fluid mb-16>
                    <v-row align="center" class="my-16">
                      <v-col cols="7" class="d-sm-none d-md-block">
                        <v-img src="@/assets/svg/undraw_Hamburger.svg"></v-img>
                      </v-col>
                      <v-col cols="5">
                        <div id="qr_code" tile>
                          <QrcodeStream
                            v-show="!loadingQR"
                            @decode="onDecode"
                            @init="onInit"
                            :camera="camera"
                          >
                            <div id="qr_placeholder">
                              <img src="@/assets/qr.png" />
                            </div>
                          </QrcodeStream>
                          <v-progress-circular
                            v-if="loadingQR"
                            :size="70"
                            :width="7"
                            color="primary"
                            indeterminate
                          ></v-progress-circular>
                          <v-btn
                            x-large
                            dark
                            color="green"
                            @click="login_chuoi"
                          >
                            <v-icon dark class="mx-0" color="white">
                              mdi-cash </v-icon
                            >LOGIN
                          </v-btn>
                        </div>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
import { QrcodeStream } from "vue-qrcode-reader";
import axios from "../../axios";
import _ from "lodash";

var pc = null;
var dc = null;

export default {
  components: {
    QrcodeStream,
  },

  data: function () {
    return {
      toggle: false,
      classes: [],
      scanScreen: false,
      camera: "off",
      loadingQR: true,
      orderItems: [
        {
          id: 1,
          name: "Bánh chuối tròn",
          price: 20000,
          quantity: 2,
        },
        {
          id: 2,
          name: "Bông lan trứng muối",
          price: 24000,
          quantity: 1,
        },
        {
          id: 3,
          name: "Bánh Thỏi vàng",
          price: 14000,
          quantity: 1,
        },
      ],
      orderItemsConfirm: [],
      totalPrice: 20000,
      user: {
        id: 0,
        full_name: "",
        username: "",
        balance: "",
      },
    };
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
      // pc.addEventListener(
      //   "icegatheringstatechange",
      //   function () {
      //     console.log("icegatheringstatechange -> ", pc.iceGatheringState);
      //   },
      //   false
      // );
      // console.log("icegatheringstatechange -> ", pc.iceGatheringState);

      // pc.addEventListener(
      //   "iceconnectionstatechange",
      //   function () {
      //     console.log("iceconnectionstatechange -> ", pc.iceConnectionState);
      //   },
      //   false
      // );
      // console.log("iceconnectionstatechange -> ", pc.iceConnectionState);

      // pc.addEventListener(
      //   "signalingstatechange",
      //   function () {
      //     console.log("signalingstatechange -> ", pc.signalingState);
      //   },
      //   false
      // );
      // console.log("signalingstatechange -> ", pc.signalingState);

      // connect audio / video
      let self = this;
      pc.addEventListener("track", function (evt) {
        if (evt.track.kind == "video")
          self.$refs.video.srcObject = evt.streams[0];
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
      let self = this;

      pc = this.createPeerConnection();

      var parameters = { ordered: true };

      dc = pc.createDataChannel("chat", parameters);

      dc.onopen = function () {
        dc.send("ping");
      };

      dc.onmessage = function (evt) {
        const data = JSON.parse(evt.data)["classes"].sort();
        if (self.classes.length != data.length) {
          console.log(1);
          self.classes = data;
        }
        if (self.classes.some((val, index) => val !== data[index])) {
          console.log(2);
          self.classes = data;
        }
      };

      // pc.ondatachannel = function (evt) {
      //   console.log("ondatachannel -> ", evt.data);
      //   evt.channel.onmessage = function (evt) {
      //     console.log("onmessage -> ", evt.data);
      //   }
      // }

      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { min: 1280, idea: 1920 },
            height: { min: 720, idea: 1080 },
            frameRate: 5,
          },
        })
        .then(
          function (stream) {
            self.$refs.stream = stream;
            stream.getTracks().forEach(function (track) {
              pc.addTrack(track, stream);
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

    stopMedia: function () {
      const self = this;
      if (this.$refs.stream) {
        self.toggle = !self.toggle;
        self.$refs.stream.getTracks().forEach((track) => {
          track.enabled = self.toggle;
        });
      }
    },

    getUserMedia: function (config) {
      return navigator.mediaDevices.getUserMedia(config);
    },

    getListVideoDevices: function () {
      return this.getListDevices().then((listDevices) => {
        return listDevices
          .filter((dev) => dev.kind == "videoinput")
          .map((dev) => dev.deviceId);
      });
    },

    getListDevices: function () {
      return navigator.mediaDevices.enumerateDevices();
    },

    onDecode(decodeString) {
      window.location.href = decodeString;
      this.scanScreen = false;
    },

    login_chuoi() {
      return axios
        .post("/api/v1/users/qr_login", "user1")
        .then((response) => {
          this.user = response.data;
          this.scanScreen = false;
        })
        .catch((e) => {
          console.log(e);
        });
    },

    async onInit(promise) {
      this.loadingQR = true;
      try {
        const { capabilities } = await promise;
        this.loadingQR = false;
        this.camera = "auto";
        console.log(capabilities);
      } catch (e) {
        console.log(e);
      }
    },

    qrLogin: function (code) {
      return axios.post("/api/v1/users/qr_login", code);
    },

    fetchItems(ids) {
      axios
        .post("/api/v1/items/fetch/", ids)
        .then((response) => {
          if (response) {
            this.orderItems = response.data;
            this.totalPrice = response.data.reduce(
              (acc, item) => acc + item.price * item.quantity,
              0
            );
          }
        })
        .catch((e) => {
          console.log(e);
        });
    },

    checkout() {
      if (this.classes == []) return;
      let orderItemsConfirm = Object.assign(this.orderItems)

      let orderDetail = {
        code: new Date().getTime(),
        user_id: this.user.id,
        total: this.totalPrice,
        order_items: [
          {
            item_id: 0,
            price: 0,
            quantity: 0,
            item_name: "string",
          },
        ],
      };

      orderDetail.order_items = orderItemsConfirm.map((item) => ({
        item_id: item.id,
        price: item.price,
        quantity: item.quantity,
        item_name: item.name,
      }));

      axios
        .post("/api/v1/orders/", orderDetail)
        .then((response) => {
          if(response.status == 200){
            this.cleanCheckout()
          }
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {});
    },

    cleanCheckout(){
      this.orderItems = []
      this.login_chuoi()
    }
  },


  created() {
    // this.$refs.video
    this.start();

    // const self = this;
    // self.getListVideoDevices().then((videoDeviceIds) => {
    //   self
    //     .getUserMedia({
    //       video: {
    //         deviceId: videoDeviceIds[1],
    //         width: 1280,
    //         height: 720,
    //         frameRate: 2,
    //       },
    //     })
    //     .then((stream) => {
    //       self.$refs.stream = stream;
    //       self.$refs.video.srcObject = stream;
    //     })
    //     .catch(console.log);
    //   // navigator.mediaDevices.getUserMedia({video:{deviceId: videoDeviceId[1]}}).then(stream => {
    //   //   self.$refs.video1.srcObject = stream
    //   // }).catch(console.log)
    // });
  },

  watch: {
    classes: _.debounce(function (newValue) {
      console.log(this.classes, newValue);
      //call api to get list items
      this.fetchItems(newValue);
    }, 500),
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

#login {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

#qr_code {
  height: 300px;
  width: 300px;
  margin: auto;
  border: 5px solid black;
  padding: 5px;
}

#qr_placeholder img {
  width: 100%;
  padding: 15px;
}
</style>