import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DictonaryApi from "@/utilities/network/dictionaryLocal";

export const useLocalDictionaryStore = defineStore({
  id: "dictionary_local",
  state: () => ({
    documents: {},
    // documentsRow: [],
  }),
  getters: {
    getByDocumentID: (state) => {
      return (docID) => state.documents[docID];
    },
    fetchIfExists: (state) => {
      return (docID, wordID, annID) => {
        if (!(docID in state.documents)) return null;
        const doc = state.documents[docID];
        if (!(wordID in doc)) return null;
        const word = doc[wordID];
        if (!(annID in word)) return null;
        return word[annID];
      };
    },
    // getRows: (state) => {
    //   return state.wordRows;
    // },
  },
  actions: {
    fetchDictionary(docID) {
      const projectStore = useProjectStore();
      return DictonaryApi.list(projectStore.getProjectInfo.id, docID).then(
        (res) => {
          const results = res.results;
          const docs = {};
          //   const docsRow = [];
          for (let item of results) {
            const docID = item["word"]["document"];
            if (!(docID in docs)) {
              docs[docID] = {};
            }
            const wordID = item["word"]["id"];
            if (!(wordID in docs[docID])) {
              docs[docID][wordID] = {};
            }
            const annID = item["annotation"];
            docs[docID][wordID][annID] = item;
            // docs[item.word] = docsRow.length;
            // docsRow.push(item);
          }
          this.documents = docs;
          console.log(docs)
          //   this.documentsRow = docsRow;
        }
      );
    },
    addWord(docID, data) {
      const projectStore = useProjectStore();
      return DictonaryApi.create(projectStore.getProjectInfo.id, data).then(
        () => {
          this.fetchDictionary(docID);
          // console.log(`added local word ${data.word}`)

          //   this.words[data.word] = this.wordRows.length;
          //   this.wordRows.push(res);
        }
      );
    },
    deleteWord(dictID) {
      const projectStore = useProjectStore();
      return DictonaryApi.delete(projectStore.getProjectInfo.id, dictID).then(
        () => {
          // console.log(`deleted local word`)
          return this.fetchDictionary();
        }
      );
    },
  },
});
