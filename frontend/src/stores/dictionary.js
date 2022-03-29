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
        for (let item in results) {
          words[results[item].word] = wordRows.length;
          wordRows.push(results[item]);
        }
        this.words = words;
        this.wordRows = wordRows;
      });
    },
    createWord(data) {
      const projectStore = useProjectStore();
      return DictonaryApi.update(projectStore.getProjectInfo.id, data).then(
        (res) => {
          this.words[data.word] = this.wordRows.length;
          this.wordRows.push(res);
        }
      );
    },
    deleteWord(data) {
      const projectStore = useProjectStore();
      return DictonaryApi.delete(
        projectStore.getProjectInfo.id,
        this.wordRows[this.words[data.word]].id
      ).then(() => {
        this.fetchDictionary();
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
