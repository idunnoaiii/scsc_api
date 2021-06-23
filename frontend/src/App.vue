<template>
    <router-view>
      <router-link to="/login" />
      <router-link to="/" />
    </router-view>
</template>

<script>
export default {
  name: "App",

  components: {},

  data: () => ({
    //
  }),
};
</script> 

<style scoped>
body {
    background-color: #251f1f;
}
</style>