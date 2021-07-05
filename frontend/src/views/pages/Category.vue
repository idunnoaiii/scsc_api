<template>
  <v-layout>
    <v-row justify="center">
      <v-col cols="8">
        <v-data-table
          :headers="headers"
          :items="categories"
          sort-by="name"
          class="elevation-1"
          width="90%"
          :search="search"
        >
          <!-- <template v-slot:[`item.stock`]="{ item }">
            <span>{{ item.stock == true ? "Yes" : "No" }}</span>
          </template>
          <template v-slot:[`item.quantity`]="{ item }">
            <span>{{ item.stock == false ? "N/A" : item.quantity }}</span>
          </template> -->
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-h4">Categories</v-toolbar-title>
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
                              v-model="editedItem.name"
                              label="Name*"
                              :rules="[required('Name')]"
                            ></v-text-field>
                          </v-col>
                        </v-row>

                        <v-row>
                          <v-col cols="12" sm="6" md="12">
                            <v-text-field
                              v-model="editedItem.description"
                              label="Description"
                            ></v-text-field>
                          </v-col>
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
                  <v-card-title class="text-h5"
                    >Are you sure you want to delete this item?</v-card-title
                  >
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="blue darken-1"
                      class="white--text"
                      @click="closeDelete"
                      >Cancel</v-btn
                    >
                    <v-btn
                      color="red darken-1"
                      class="white--text"
                      @click="deleteItemConfirm"
                      >OK</v-btn
                    >
                    <v-spacer></v-spacer>
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
    search: "",
    dialogDelete: false,
    headers: [
      {
        text: "Name",
        align: "start",
        value: "name",
      },
      { text: "Description", value: "description" },
      { text: "Action", value: "actions", sortable: false },
    ],
    categories: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      description: "",
    },
    defaultItem: {
      full_name: "",
      username: "",
      role: "",
    },
    categorySelected: false,
    required(inputName) {
      return (v) =>
        (v && v.toString().length > 0) || `${inputName} is required.`;
    },
    noSpace() {
      return (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed";
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Category" : "Edit Category";
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
        .get("api/v1/categories/")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    onFileSelected(file) {
      this.selectedFile = file;
    },

    editItem(item) {
      this.editedIndex = this.categories.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.password = "";
    },

    deleteItem(item) {
      this.editedIndex = this.categories.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      // this.items.splice(this.editedIndex, 1);
      axios
        .delete(`/api/v1/categories/${this.editedItem.id}`)
        .then((response) => {
          if (response.status == 200) {
            this.$swal.fire({
              icon: "success",
              title: "Delete item successfully",
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

      const item_added = {
        name: this.editedItem.name,
        description: this.editedItem.description,
      };

      if (this.editedIndex > -1) {
        // update
        //if update action then add id to item for notice
        item_added.id = this.editedItem.id;
        axios
          .put("/api/v1/categories/", item_added)
          .then((response) => {
            if (response.status == 200) {
              this.$swal({
                icon: "success",
                title: "Update new item successfully",
              });
              this.load();
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        // insert
        axios.post("/api/v1/categories/", item_added).then((response) => {
          if (response.status == 200) {
            this.$swal({
              icon: "success",
              title: "Add new item successfully",
            });
            this.load();
          }
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