<template>
  <v-app id="login">
    <v-main >
      <v-container  fluid fill-height>
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
                  >
                  </v-text-field>
                  <v-text-field
                    id="password"
                    prepend-icon="lock"
                    name="password"
                    label="Mật khẩu"
                    type="password"
                  >
                  </v-text-field>
                  <v-alert
                    v-if="err"
                    border="left"
                    color="red"
                    dismissible
                    type="error"
                    transition="scale-transition"
                    >Sai tên đăng nhập hoặc mật khẩu!
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
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "Login",
  props: {
    source: String,
  },
  data() {
    return {
      err: false,
    };
  },
  methods: {
    login: function () {
      this.$router.push('/')
    },
  },
};
</script>


<style scoped>
  #login {
    background: linear-gradient(40deg,#77008cde,#041158ec);
  }
</style>