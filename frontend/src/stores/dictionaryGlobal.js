import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DictonaryApi from "@/utilities/network/dictionary";

export const useDictionaryStore = defineStore({
  id: "dictionary",
  state: () => ({
    words: {},
    wordRows: [],
  }),
  getters: {
    getWords: (state) => {
      return state.words;
    },
    getRows: (state) => {
      return state.wordRows;
    },
  },
  actions: {
    fetchDictionary() {
      const projectStore = useProjectStore();
      return DictonaryApi.list(projectStore.getProjectInfo.id).then((res) => {
        const results = res.results;
        const words = {};
        const wordRows = [];
        for (let item of results) {
          words[item.word] = wordRows.length;
          wordRows.push(item);
        }
        this.words = words;
        this.wordRows = wordRows;
      });
    },
    createWord(data) {
      const projectStore = useProjectStore();
      return DictonaryApi.create(projectStore.getProjectInfo.id, data).then(
        (res) => {
          this.words[data.word] = this.wordRows.length;
          this.wordRows.push(res);
        }
      );
    },
    deleteWord(word) {
      const projectStore = useProjectStore();
      return DictonaryApi.delete(
        projectStore.getProjectInfo.id,
        this.wordRows[this.words[word]].id
      ).then(() => {
        return this.fetchDictionary();
      });
    },
    updateWord(data) {
      const projectStore = useProjectStore();
      return DictonaryApi.update(projectStore.getProjectInfo.id, data).then(
        () => {
          this.wordRows[this.words[data.word]] = data;
        }
      );
    },
  },
});
