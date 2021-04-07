// import axios from "axios";

// const api = axios.create({});

const api = {
  get(url) {
    let data = {};

    switch (url) {
      case "/user":
        data = {
          id: "123",
          name: "Some Buddy",
          initials: "SB",
          organisation: {
            id: 321,
          },
        };
        break;

      case "/feed":
        data = [
          {
            text: "Something in the feed",
            path: "/projects",
          },
        ];
        break;

      case "/overview":
        data = [
          {
            number: 1234,
            object: "segments",
          },
          {
            number: 50,
            object: "team",
          },
          {
            number: 5,
            object: "languages",
          },
          {
            number: 4,
            object: "projects",
          },
        ];
        break;

      case "/organisations":
        data = [
          {
            id: 123,
            name: "Organisation 1",
          },
          {
            id: 321,
            name: "Organisation 2",
          },
        ];
    }

    return Promise.resolve({ data });
  },
};

export default api;
