import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DictonaryApi from "@/utilities/network/dictionaryGlobal";

export const useGlobalDictionaryStore = defineStore({
  id: "dictionary_global",
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
    containsWord: (state) => {
      return (word) => {
        return word in state.words;
      };
    },
  },
  actions: {
    fetchDictionary(q = undefined) {
      const projectStore = useProjectStore();
      return DictonaryApi.list(projectStore.getProjectInfo.id, q).then(
        (res) => {
          const results = res.results;
          const words = {};
          const wordRows = [];
          for (let item of results) {
            words[item.word] = wordRows.length;
            wordRows.push(item);
          }
          this.words = words;
          this.wordRows = wordRows;
        }
      );
    },
    addWord(word, modification_type, ground_truth_label) {
      const projectStore = useProjectStore();
      return DictonaryApi.create(projectStore.getProjectInfo.id, {
        word,
        modification_type,
        ground_truth_label,
      }).then((res) => {
        this.words[word] = this.wordRows.length;
        this.wordRows.push(res);
        console.log(`added global word ${word}`)
      });
    },
    deleteWord(word) {
      console.log(`deleted global word ${word}`)
      const projectStore = useProjectStore();
      return DictonaryApi.delete(
        projectStore.getProjectInfo.id,
        this.wordRows[this.words[word]].id
      ).then(() => {
        return this.fetchDictionary();
      });
    },
  },
});
