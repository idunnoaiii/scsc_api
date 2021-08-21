<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="10">
        <v-data-table
          :headers="headers"
          :items="users"
          sort-by="calories"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <template v-slot:[`item.role_value`]="{ item }">
            <span>{{ getRoleName(item.role_id) }}</span>
          </template>
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4"> Users </v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-text-field
                v-model="search"
                label="Search"
                hide-details
                class="mx-4"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    New
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-form ref="form" lazy-validation v-model="valid">
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.full_name"
                              label="Name"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.username"
                              :disabled="editedIndex !== -1"
                              label="Username*"
                              :rules="[required('Username'), noSpace()]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" md="12" v-if="editedIndex === -1">
                            <v-text-field
                              v-model="password"
                              label="Password*"
                              type="Password"
                              :rules="[required('Password')]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" md="12">
                            <v-select
                              :items="roles"
                              v-model="editedItem.role_id"
                              label="Role*"
                              :rules="[
                                (v) =>
                                  (v != null && v != undefined && v != 0) ||
                                  'Roles is required.',
                              ]"
                            ></v-select>
                          </v-col>

                          <!-- <v-col cols="12" sm="6" md="12">
                          <v-text-field
                            v-model="editedItem.role"
                            label="Role"
                          ></v-text-field>
                        </v-col> -->
                        </v-row>
                      </v-container>
                    </v-form>
                    <small>*indicates required field</small>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="close"
                      text
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="green darken-1"
                      class="white--text"
                      @click="save"
                      :disabled="!valid"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5"> Warning! </v-card-title>
                  <v-card-text>You want to delete this user?</v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary darken-1" text @click="closeDelete">
                      Cancel
                    </v-btn>
                    <v-btn
                      color="red darken-1"
                      class="white--text"
                      @click="deleteItemConfirm"
                    >
                      OK
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="primary" @click="load"> Reset </v-btn>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-layout>
</template>
<script>
import axios from "../../axios";
export default {
  data: () => ({
    valid: true,
    dialog: false,
    password: "",
    search: "",
    dialogDelete: false,
    headers: [
      {
        text: "Full Name",
        align: "start",
        value: "full_name",
      },
      { text: "Username", value: "username" },
      { text: "Role", value: "role_value", sortable: false },
      { text: "Action", value: "actions", sortable: false },
    ],
    users: [],
    editedIndex: -1,
    editedItem: {
      full_name: "",
      username: "",
      role_id: 0,
    },
    defaultItem: {
      full_name: "",
      username: "",
      role_id: 0,
    },
    roles: [
      {
        text: "",
        value: 0,
      },
      {
        text: "Cashier",
        value: 0,
      },
    ],
    roleSelected: 0,
    required(inputName) {
      return (v) => (v && v.length > 0) || `${inputName} is required.`;
    },
    noSpace() {
      return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New User" : "Edit User";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  // created() {
  //   this.initialize();
  // },

  mounted() {
    this.load();
  },
  methods: {
    load() {
      axios
        .get("api/v1/users/?skip=0&limit=100")
        .then((response) => {
          this.users = response.data;
          for (let u of this.users) {
            u.is_admin = u.role_id == 1;
          }
          console.log(this.users);
        })
        .catch((err) => {
          console.log(err);
        });
      axios
        .get("api/v1/users/roles")
        .then((response) => {
          if (response.status == 200) {
            this.roles = response.data.map((r) => ({
              value: r.id,
              text: r.name,
            }));
            console.log(this.roles);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getRoleName(id) {
      let v = this.roles?.reduce((acc, cur) => {
          if(cur.value == id){
            acc = cur.text;
          }
          return acc;
        }, "");
      return v;
    },

    editItem(item) {
      this.editedIndex = this.users.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.password = "";
    },

    deleteItem(item) {
      this.editedIndex = this.users.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.users.splice(this.editedIndex, 1);
      axios
        .delete(`/api/v1/users/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
            this.$store.commit("SET_TOAST", {
              toastMsg: "User deleted!",
              toastColor: "green",
            });
            this.load();
          }
        })
        .catch((err) => {
          console.log(err);
        });

      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$refs.form.reset();
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (!this.$refs.form.validate()) {
        return;
      }

      const userObj = {
        full_name: this.editedItem.full_name,
        role_id: this.editedItem.role_id,
      };

      if (this.editedIndex > -1) {
        //update
        userObj.id = this.editedItem.id;
        axios
          .put("/api/v1/users/", userObj)
          .then(() => {
            this.load();
            this.$store.commit("SET_TOAST", {
              toastMsg: "Item updated!",
              toastColor: "green",
            });
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        //add

        userObj.password = this.password;
        userObj.username = this.editedItem.username;
        userObj.role_id = this.editedItem.role_id;

        axios
          .post("/api/v1/users/", userObj)
          .then(() => {
            this.load();
            this.$store.commit("SET_TOAST", {
              toastMsg: "User added!",
              toastColor: "green",
            });
          })
          .catch((err) => {
            console.log(err);
          });
      }
      this.close();
    },

    filterUser(value, search, items) {
      console.log(items);
      return (
        value != null &&
        search != null &&
        typeof value === "string" &&
        value.toString().indexOf(search) !== -1
      );
    },
  },
};
</script>