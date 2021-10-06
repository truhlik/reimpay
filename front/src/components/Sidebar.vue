<template>
  <div class="app-sidebar sidebar-shadow"
       @mouseover="toggleSidebarHover('add','closed-sidebar-open')"
       @mouseleave="toggleSidebarHover('remove','closed-sidebar-open')">
    <div class="app-header__logo">
      <img src="~/assets/img/logos/color_wide.png" alt="logo" class="only-open">
      <div class="header__pane ml-auto">
        <button
          :class="{ 'is-active' : isOpen }" @click="toggleBodyClass('closed-sidebar')"
          class="hamburger close-sidebar-btn hamburger--elastic"
          ref="hamburgerBtn"
          type="button"
        >
          <span class="hamburger-box">
            <span class="hamburger-inner"></span>
          </span>
        </button>
      </div>
    </div>
    <div class="app-sidebar-content">
      <VuePerfectScrollbar class="app-sidebar-scroll">
        <SidebarMenu :menu="menu" :showChild="true" @item-click="toggleHamburger()"/>
      </VuePerfectScrollbar>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import { SidebarMenu } from 'vue-sidebar-menu'
  import VuePerfectScrollbar from 'vue-perfect-scrollbar'

  import getMenuItems from '~/helpers/getMenuItems'

  export default {
    components: {
      SidebarMenu,
      VuePerfectScrollbar
    },
    computed: {
      ...mapState({
        studyList: state => state.studies.studyList,
        user: state => state.account.user,
      }),
      menu() {
        return getMenuItems(this)
      },
    },
    data() {
      return {
        collapsed: true,
        isOpen: false,
        sidebarActive: false,
        windowWidth: 0,
      }
    },
    methods: {
      ...mapActions({
        getStudyList: 'studies/getStudyList'
      }),
      toggleBodyClass(className) {
        const el = document.body;
        this.isOpen = !this.isOpen;
        this.isOpen ? el.classList.add(className) :el.classList.remove(className)
      },
      toggleHamburger() {
        document.querySelector('.close-sidebar-btn').click()  // for some reason '$refs' not working
      },
      toggleSidebarHover(add, className) {
        const el = document.body;
        this.sidebarActive = !this.sidebarActive;

        this.windowWidth = document.documentElement.clientWidth;

        if (this.windowWidth > '992') {
          add === 'add' ? el.classList.add(className) : el.classList.remove(className);
        }
      },
      getWindowWidth(event) {
        const el = document.body;

        this.windowWidth = document.documentElement.clientWidth;

        if (this.windowWidth < '1350') {
          el.classList.add('closed-sidebar', 'closed-sidebar-md');
        } else {
          el.classList.remove('closed-sidebar', 'closed-sidebar-md');
        }
      },
    },
    mounted() {
      this.getStudyList();

      this.$nextTick(function () {
        window.addEventListener('resize', this.getWindowWidth);
        //Init
        this.getWindowWidth()
      })
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.getWindowWidth);
    }
  }
</script>

<style lang="scss">
  .only-closed, .only-open {
    transition: all 0.5s ease-in-out;
  }

  .closed-sidebar:not(.closed-sidebar-open) {
    .app-header__logo img {
      margin-left: -5px;
      width: 250px;
    }
  }

  .closed-sidebar-open:not(.closed-sidebar) {
    .app-header__logo img {
      width: 180px;
    }
  }

  .app-header__logo img {
    margin-right: 10px;
    width: 180px;
  }
</style>
