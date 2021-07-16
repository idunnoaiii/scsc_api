<template >
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" md="6">
        <v-card class="elevation-12 rounded-xl">
          <v-card-text>
            <v-container fluid>
              <v-row align="center" class="my-16">
                <v-col cols="6" class="d-sm-none d-md-block">
                  <v-img src="@/assets/svg/login.svg"></v-img>
                </v-col>
                <v-col cols="6" md="6" sm="12">
                  <div class="text-center mb-8">
                    <h3 class="text-h4">Welcome</h3>
                    <h4 class="subtitle-1 mb-3">Have a good day!</h4>
                  </div>
                  <v-form>
                    <v-text-field
                      prepend-icon="person"
                      name="login"
                      label="Username"
                      type="text"
                      class="mx-8"
                      v-model="username"
                      outlined
                      dense
                      @keyup.enter="login"
                    >
                    </v-text-field>
                    <v-text-field
                      id="password"
                      prepend-icon="lock"
                      name="password"
                      label="Password"
                      type="password"
                      class="mx-8"
                      v-model="password"
                      outlined
                      dense
                      @keyup.enter="login"
                    >
                    </v-text-field>
                    <div class="d-flex">
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        @click="login"
                        class="text-none mx-8"
                        >Login</v-btn
                      >
                    </div>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar
      :timeout="2000"
      v-model="snackbar"
      :color="snackbarColor"
      absolute
      right
      top
      text
      prominent
      transition="slide-x-reverse-transition"
    >
      {{ snackbarMsg }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { setLocalToken } from "../../utils";
import axios from "../../axios";

export default {
  name: "Login",
  props: {
    source: String,
  },
  data() {
    return {
      err: false,
      username: "",
      password: "",
      snackbar: false,
      snackbarMsg: "",
      snackbarColor: "",
    };
  },
  methods: {
    login: function () {
      if (this.username == "" || this.password == "") {
        this.snackbar = true;
        this.snackbarMsg = "Please input username and password";
        this.snackbarColor = "warning";
        return;
      }

      const params = new URLSearchParams();
      params.append("username", this.username);
      params.append("password", this.password);
      axios
        .post("/api/v1/login/access-token", params)
        .then((response) => {
          const token = response.data.access_token;
          if (token) {
            setLocalToken(token);
            this.$store.commit("SET_LOGIN_TOKEN", token);
            this.$store.commit("SET_AUTH_STATUS", true);
            this.$store.commit("SET_ROLE", true);
            this.$router.replace("/");
          }
        })
        .catch(() => {
          this.snackbar = true;
          this.snackbarMsg = "Username or password is not correct!";
          this.snackbarColor = "red";
        });
    },
  },
  beforeCreate() {
    if (localStorage.getItem("token")) {
      this.$router.replace("/");
    }
  },
};
</script>


<style scoped>
#login {
  background: #a3b4c525;
}
</style>