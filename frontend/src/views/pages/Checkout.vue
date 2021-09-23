<template>
  <v-layout>
    <v-col lg="8">
      <v-card
        outline
        class="d-flex flex-column justify-md-space-between"
        height="100%"
      >
        <v-card color="primary">
          <v-toolbar dark color="primary">
            <v-toolbar-title class="text-h4">SCSC</v-toolbar-title>
            <v-spacer></v-spacer>
            <span class="text-h6">{{ user.full_name }}</span>
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
        <div
          class="d-flex justify-lg-space-around pa-6"
          style="background: #1976d2"
        >
          <v-btn x-large dark id="toggle" color="orange" @click="exit">
            <v-icon dark class="mx-0" color="white"> mdi-cancel </v-icon>
            EXIT
          </v-btn>
          <!-- <v-btn x-large dark id="toggle" color="orange" @click="stop">
            <v-icon dark class="mx-0" color="white"> mdi-cancel </v-icon>
            STOP
          </v-btn> -->
          <v-btn
            x-large
            dark
            color="green"
            id="start"
            @click="checkout"
            :loading="debounceBtnCheckout"
            :disabled="!canCheckout"
          >
            <v-icon dark class="mx-0" color="white"> mdi-cash </v-icon>
            CHECKOUT
          </v-btn>
        </div>
      </v-card>
    </v-col>
    <v-col lg="4">
      <v-card
        outline
        height="100%"
        class="d-flex flex-column justify-lg-space-between"
      >
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

        <v-card class="py-8" color="primary">
          <v-card-actions class="d-flex-row">
            <div class="text-h5 d-inline-flex px-5 white--text">
              Total Price:
            </div>
            <div class="text-h5 d-inline-flex px-5 white--text" white--text>
              {{ totalPrice | currency }}
            </div>
          </v-card-actions>
          <v-card-actions class="d-flex-row">
            <div class="text-h5 d-inline-flex px-5 white--text">Balance:</div>
            <div class="text-h5 d-inline-flex px-5 white--text">
              {{ user.balance | currency }}
            </div>
          </v-card-actions>
        </v-card>
      </v-card>
    </v-col>
    <v-dialog v-model="scanScreen" fullscreen hide-overlay persistent>
      <v-card color="primary">
        <v-container id="login" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="10">
              <div class="rounded-xl">
                <v-card-title class="justify-center">
                  <div class="text-center my-10">
                    <div class="text-h2 white--text">SCSC Welcome</div>
                  </div>
                </v-card-title>
                <v-card-text>
                  <v-container fluid mb-16>
                    <v-row align="center" class="my-16">
                      <v-col cols="7" class="d-sm-none d-md-block">
                        <v-img src="@/assets/svg/undraw_Hamburger.svg"></v-img>
                      </v-col>
                      <v-col cols="5">
                        <div id="qr_code" class="d-flex" tile>
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
                            color="white"
                            indeterminate
                            style="margin: auto"
                          ></v-progress-circular>
                        </div>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
              </div>
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
      debounceBtnCheckout: true,
      canCheckout: false,
      toggle: false,
      postCheckout: true,
      classes: [],
      scanScreen: true,
      camera: "off",
      loadingQR: true,
      orderItems: [],
      orderItemsConfirm: [],
      totalPrice: 0,
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
      var config = {
        sdpSemantics: "unified-plan",
      };

      config.iceServers = [
        {
          urls: "stun:vc.example.com:3478",
        },
        {
          urls: "turn:vc.example.com:3478",
          username: "coturnUser",
          credential: "coturnUserPassword",
        },
      ];

      pc = new RTCPeerConnection(config);

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
          console.log(e);
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
          self.classes = data;
        }
        if (self.classes.some((val, index) => val !== data[index])) {
          self.classes = data;
        }
      };

      navigator.mediaDevices
        .getUserMedia({
          video: {
            width: { min: 1280, idea: 1280 },
            height: { min: 720, idea: 720 },
            frameRate: 4,
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
      this.camera = "off";
      setTimeout(function () {
        this.camera = "auto";
      }, 1000);
      axios
        .post("/api/v1/users/qr_login", decodeString)
        .then((response) => {
          if (response.data) {
            this.user = response.data;
            this.scanScreen = false;
            dc.send("True");
          } else {
            this.$store.commit("SET_TOAST", {
              toastMsg: "Can not regconize user code!",
              toastColor: "red",
            });
          }
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
      const self = this;

      axios
        .post("/api/v1/items/fetch/", ids)
        .then((response) => {
          if (response) {
            this.orderItems = response.data;
            this.totalPrice = response.data.reduce(
              (acc, item) => acc + item.price * item.quantity,
              0
            );
            this.canCheckout =
              this.user.balance >= this.totalPrice && this.items != [];
            if (this.user.balance < this.totalPrice) {
              this.$swal.fire({
                title: "Balance not enough to checkout!",
                icon: "warning",
                showConfirmButton: false,
              });
            }
          }
        })
        .catch((e) => {
          console.log(e);
        })
        .finally(() => {
          setTimeout(() => {
            self.debounceBtnCheckout = false;
          }, 2000);
        });
    },

    checkout() {
      if (this.classes == []) return;
      let orderItemsConfirm = Object.assign(this.orderItems);

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
          if (response.status == 200) {
            this.cleanCheckout();
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    exit() {
      this.scanScreen = true;
      this.orderItems = [];
      this.classes = [];
      this.user = {
        id: 0,
        full_name: "",
        username: "",
        balance: "",
      };
      dc.send("False");
    },

    cleanCheckout() {
      this.$swal
        .fire({
          title: "Checkout successed!",
          icon: "success",
          showConfirmButton: false,
          timer: 1000,
        })
        .then((result) => {
          if (result.dismiss === this.$swal.DismissReason.timer) {
            this.exit();
          }
        });
    },
  },

  created() {
    this.start();
  },

  watch: {
    classes: _.debounce(function (newValue) {
      //call api to get list items
      this.debounceBtnCheckout = true;
      this.fetchItems(newValue);
    }, 1000),
  },

  filters: {
    currency(value) {
      return value.toLocaleString();
    },
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
  border: 5px solid white;
  border-radius: 15px;
  padding: 5px;
}
.qrcode-stream-wrapper video {
  border-radius: 15px;
}

#qr_placeholder img {
  width: 100%;
  padding: 15px;
  background: rgba(255, 255, 255, 0.137);
}
</style>