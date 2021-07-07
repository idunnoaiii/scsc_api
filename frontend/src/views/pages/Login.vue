<template>
  <v-layout>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm6 md3>
          <v-card class="elevation-4">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Đăng nhập</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="py-4">
              <v-form>
                <v-text-field
                  prepend-icon="person"
                  name="login"
                  label="Tên đăng nhập"
                  type="text"
                  class="elevation-0"
                  v-model="username"
                >
                </v-text-field>
                <v-text-field
                  id="password"
                  prepend-icon="lock"
                  name="password"
                  label="Mật khẩu"
                  type="password"
                  v-model="password"
                >
                </v-text-field>
                <v-alert
                  v-if="err"
                  border="left"
                  color="red"
                  dismissible
                  type="error"
                  transition="scale-transition"
                  >Incorect username or password!
                </v-alert>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" tile @click="login">Đăng nhập</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-layout>
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
    };
  },
  methods: {
    login: function () {
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
            this.$router.push("/");
          }
        })
        .catch((err) => console.log(err));
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
  background: transparent;
}
</style>