 
 <template>
  <v-row justify="center">
    <v-dialog v-model="$store.state.changePassword" max-width="640px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Change password</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" lazy-validation v-model="valid">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="Current password*"
                    v-model="changePassowrd.curPassword"
                    type="password"
                    :rules="[required('Current password')]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="New password*"
                    v-model="changePassowrd.newPassword1"
                    type="password"
                    :rules="[required('New password')]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Retype new password*"
                    v-model="changePassowrd.newPassword2"
                    type="password"
                    :rules="[required('Current password'), matchPassword()]"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-divider class="mb-4"></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary darken-1"
            class="white--text"
            @click="$store.commit('SET_CHANGE_PASSWORD', null)"
          >
            Close
          </v-btn>
          <v-btn
            color="green darken-1"
            class="white--text"
            @click="updatePassowrd"
          >
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from "../axios";
export default {
  props: {
    username: String,
  },
  data: function () {
    return {
      valid: true,
      changePassowrd: {
        curPassword: "",
        newPassword1: "",
        newPassword2: "",
      },
      required(inputName) {
        return (v) =>
          (v && v.toString().length > 0) || `${inputName} is required.`;
      },
      matchPassword() {
        return (v) =>
          (v && v == this.changePassowrd.newPassword1) ||
          `New password not matched!`;
      },
    };
  },
  methods: {
    updatePassowrd: function () {
      if (!this.$refs.form.validate()) {
        return;
      }
      console.log("VO");
      axios
        .put(
          "api/v1/users/change-password",
          JSON.stringify({
            username: this.username,
            password: this.changePassowrd.curPassword,
            new_password: this.changePassowrd.newPassword1,
          })
        )
        .then((res) => {
          if (res.status == 200) {
            this.$store.commit("SET_TOAST", {
              toastMsg: "Change password successfully",
              toastColor: "success",
            });
            this.$store.commit("SET_CHANGE_PASSWORD", null);
            return;
          }
        })
        .catch(() => {
          this.$store.commit("SET_TOAST", {
            toastMsg: "Password is not correct",
            toastColor: "orange",
          });
          return;
        });
    },
  },
  mounted() {
    console.log(this.username);
  },
};
</script>
