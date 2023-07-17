const { createApp } = Vue;
createApp({
  data() {
    return {
      data: "",
      toxicLevel: "",
      statArr: [],
      st: {},
      groupList: [],
      allComments: [],
      toxicComments: [],
      showComments: false,
      showToxic: false,
      comments: "",
      postCount: "",
      isLoading: false,
      mode: "post",
      statistics: {},
      isOpen: false,
      selModel: '',
      globSt: { toxic: 0, all: 0, non_toxic: 0, toxic_rate: 0 }
    };
  },
  computed: {
    getPlaceholder() {
      return this.mode === "post"
        ? "Ссылка на пост (https://t.me/channel/post-id)"
        : "Ссылка на группу (https://t.me/channel)";
    },
    getToxicRate() {
      const stArr = []
      this.statArr.forEach(el => { stArr.push(el[0]) })
      return stArr.sort((a, b) => +b.toxic_rate - +a.toxic_rate)
    }
  },
  methods: {
    reset() {
      this.data = "",
      this.toxicLevel = "",
      this.statArr = [],
      this.st = {},
      this.groupList = [],
      this.allComments = [],
      this.toxicComments = [],
      this.showComments = false,
      this.showToxic = false,
      this.comments = "",
      this.postCount = "",
      this.statistics = {},
      this.selModel = '',
      this.globSt = { toxic: 0, all: 0, non_toxic: 0, toxic_rate: 0 }
    },
    addGroup() {
      this.groupList.push({ group: this.data.split('/').reverse()[0], posts: this.postCount })
      this.postCount = "";
      this.data = "";
    },
    async getData() {
      this.isLoading = true;
      const linkData = this.data.split("/").reverse();
      let out = []
      switch (this.mode) {
        case "post":
          out = await eel.get_data(true, this.postCount, linkData[1], linkData[0])();
          break;
        case "group":
          out = await eel.get_data(false, this.postCount, linkData[0])();
          break;
      }
      console.log(out);
      this.isLoading = false;
      this.postCount = "";
      this.statArr.push(out)
      this.data = "";
      this.st = this.statArr[0][0];
      this.allComments = this.statArr[0][1];
      this.allComments.forEach((el) => {
        el.toxic_rate = parseFloat(el.toxic_rate);
        if (el.toxic_rate > 0.75) {
          this.toxicComments.push(el);
        }
      });
      this.toxicLevel = this.st.toxic_rate;
    },
    async deepSearch() {
      this.isLoading = true;
      let counter = 0
      await this.groupList.forEach(async el => {
        const res = await eel.get_data(false, el.posts, el.group)();
        this.statArr.push(res)
        counter += 1
        if (counter === this.groupList.length) {
          this.isLoading = false;
          this.postCount = "";
          this.data = "";
          this.selModel = this.groupList[0].group
          this.st = this.statArr[0][0];
          this.allComments = this.statArr[0][1];
          this.allComments.forEach((el) => {
            el.toxic_rate = parseFloat(el.toxic_rate);
            if (el.toxic_rate > 0.75) {
              this.toxicComments.push(el);
            }
          });
          this.toxicLevel = this.st.toxic_rate;
          this.statArr.forEach(el => {
            this.globSt.toxic += +el[0].toxic
            this.globSt.non_toxic += +el[0].non_toxic
            this.globSt.all += +el[0].all
          })
          this.globSt.toxic_rate = Math.round((this.globSt.toxic * 100) / this.globSt.all)
          console.log((this.globSt.toxic * 100), this.globSt.all, this.globSt.toxic_rate);
        }
      })
    }
  },
  mounted() {
    document.addEventListener('click', evt => {
      const target = evt.target

      if (!target.closest('.select'))
        this.isOpen = false
      if (target.closest('.select-item')) {
        this.selModel = target.dataset.item
        const idx = +target.dataset.idx
        this.st = this.statArr[idx][0];
        this.allComments = this.statArr[idx][1];
        this.allComments.forEach((el) => {
          el.toxic_rate = parseFloat(el.toxic_rate);
          if (el.toxic_rate > 0.75) {
            this.toxicComments.push(el);
          }
        });
        this.toxicLevel = this.st.toxic_rate;
        this.isOpen = false
      }
    })
  },
}).mount("#app");
