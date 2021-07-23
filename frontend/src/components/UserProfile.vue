 
 <template>
  <v-row justify="center">
    <v-dialog v-model="$store.state.userProfile" max-width="640px">
      <v-card>
        <v-toolbar color="primary">
          <v-card-title>
            <span class="text-h5 white--text">User Profile</span>
          </v-card-title>
          <v-spacer></v-spacer>
          <v-btn
            color="warning"
            class="white--text"
            @click="$store.commit('SET_CHANGE_PASSWORD', null)"
          >
            Change Password
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <v-form ref="form" lazy-validation v-model="valid">
            <v-container>
              <v-row>
                <v-col cols="4"></v-col>
                <v-col cols="4">
                  <v-img src="@/assets/svg/useravatar.svg"></v-img>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    placeholder="Username"
                    label="Username*"
                    :value="userProfile.username"
                    readonly
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Fullname*"
                    placeholder="Fullname*"
                    :rules="[required('Fullname')]"
                    v-model="userProfile.full_name"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-radio-group v-model="userProfile.gender" row>
                    <template v-slot:label>
                      <div>Gender</div>
                    </template>
                    <v-radio label="Male" :value="true"></v-radio>
                    <v-radio label="Female" :value="false"></v-radio>
                  </v-radio-group>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    placeholder="Address"
                    v-model="userProfile.address"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    placeholder="Contact"
                    v-model="userProfile.contact"
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
            @click="$store.commit('SET_USER_PROFILE', null)"
          >
            Close
          </v-btn>
          <v-btn
            color="green darken-1"
            class="white--text"
            @click="updateUserProfile"
          >
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <ChangePassword
      v-if="$store.state.changePassword"
      :username="userProfile.username"
    ></ChangePassword>
  </v-row>
</template>
<script>
import axios from "../axios";
import ChangePassword from "./ChangePassword.vue";
export default {
  components: {
    ChangePassword,
  },
  data: function () {
    return {
      valid: true,
      userProfile: {
        id: 0,
        username: "",
        full_name: "",
        contact: "",
        address: "",
        gender: false,
      },
      required(inputName) {
        return (v) =>
          (v && v.toString().length > 0) || `${inputName} is required.`;
      },
    };
  },
  methods: {
    updateUserProfile: function () {
      if (this.userProfile.id == 0) return;

      if (!this.$refs.form.validate()) {
        return;
      }

      axios
        .put("api/v1/users/", this.userProfile)
        .then((res) => {
          if (res.status == 200) {
            alert("OK");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    var userid = this.$store.state.userid;
    axios
      .get("api/v1/users/" + userid)
      .then((res) => {
        this.userProfile = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
