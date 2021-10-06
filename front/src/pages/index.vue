<template>
  <div class="container">
    <div class="index-content">
      <Logo />
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo
  }
}
</script>

<style scoped lang="scss">
.container {
  align-items: center;
  display: flex;
  justify-content: center;
  margin: 0 auto;
  min-height: 80vh;
  text-align: center;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  word-spacing: 5px;
  padding-bottom: 15px;
}


.index-content {
  animation: turn 2s ease-in-out forwards 0s;
  max-width: 100%;
  transform: rotateY(90deg);
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}

</style>
