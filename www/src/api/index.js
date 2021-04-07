// import axios from "axios";

// const api = axios.create({});

const api = {
  get(url) {
    let data = {};

    const orgId = 123;

    switch (url) {
      case "/user":
        data = {
          id: "123",
          name: "Some Buddy",
          initials: "SB",
          organisation: {
            id: orgId,
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
        break;

      case `/organisation/${orgId}/projects`:
        data = [
          {
            id: 2,
            name: "Mobile",
          },
          {
            id: 24,
            name: "Web",
          },
        ];
        break;
    }

    return Promise.resolve({ data });
  },
};

export default api;
