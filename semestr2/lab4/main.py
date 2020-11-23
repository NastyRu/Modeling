import numpy.random as rn


class RandomGenerator:
    def __init__(self, a, b, mu, sigma):
        self.a = a
        self.b = b
        self.mu = mu
        self.sigma = sigma

    def uniform_random(self):
        return rn.uniform(self.a, self.b)

    def normal_random(self):
        return rn.normal(self.mu, self.sigma)


class GenerateRequest:
    def __init__(self, generator, count):
        self.generator = generator
        self.num_requests = count

    def generate_request(self):
        self.num_requests -= 1

    def delay(self):
        time = -1
        while time < 0:
            time = self.generator.uniform_random()
        return time


class ProcessRequest:
    def __init__(self, generator, p):
        self.generator = generator
        self.queue, self.received, self.max_queue, self.reenters, self.processed = 0, 0, 0, 0, 0
        self.p = p

    def receive_request(self):
        self.queue += 1
        self.received += 1
        self.max_queue = max(self.max_queue, self.queue)

    def delay(self):
        time = -1
        while time < 0:
            time = self.generator.normal_random()
        return time

    def process(self):
        if self.queue > 0:
            self.queue -= 1
            self.processed += 1
        if rn.random_sample() < self.p:
            self.reenters += 1
            self.receive_request()


class Model:
    def __init__(self, generator, processor):
        self.generator = generator
        self.processor = processor

    def dt_principle(self, dt):
        generated_time = self.generator.delay()
        processed_time = generated_time + self.processor.delay()
        current_time = 0
        num_requests = self.generator.num_requests

        while self.processor.processed < num_requests + self.processor.reenters:
            if generated_time < current_time:
                self.generator.generate_request()
                self.processor.receive_request()
                generated_time += self.generator.delay()
            if processed_time < current_time:
                self.processor.process()
                if self.processor.queue > 0:
                    processed_time += self.processor.delay()
                else:
                    processed_time = generated_time + self.processor.delay()
            current_time += dt

        result = {"Processed requests": self.processor.processed,
                  "Reenters requests": self.processor.reenters,
                  "Max queue": self.processor.max_queue,
                  "Processed time": current_time}

        return result

    def event_principle(self):
        generated_time = self.generator.delay()
        processed_time = generated_time + self.processor.delay()
        num_requests = self.generator.num_requests

        while self.processor.processed < num_requests + self.processor.reenters:
            if generated_time <= processed_time:
                self.generator.generate_request()
                self.processor.receive_request()
                generated_time += self.generator.delay()
            else:
                self.processor.process()
                if self.processor.queue > 0:
                    processed_time += self.processor.delay()
                else:
                    processed_time = generated_time + self.processor.delay()

        result = {"Processed requests": self.processor.processed,
                  "Reenters requests": self.processor.reenters,
                  "Max queue": self.processor.max_queue,
                  "Processed time": processed_time}

        return result


if __name__ == '__main__':
    a = 1
    b = 10
    mu = 0
    sigma = 1
    n = 1000
    p = 0.99
    dt = 1
    random_generator = RandomGenerator(a, b, mu, sigma)
    generator = GenerateRequest(random_generator, n)
    processor = ProcessRequest(random_generator, p)
    model = Model(generator, processor)
    result = model.dt_principle(dt)
    print("Принцип дельта Т\n")
    print(f"Обработанные заявки: {result['Processed requests']}")
    print(f"Повторно обработанные заявки: {result['Reenters requests']}")
    print(f"Длина очереди: {result['Max queue']}")
    print(f"Время обработки: {result['Processed time']}")

    random_generator = RandomGenerator(a, b, mu, sigma)
    generator = GenerateRequest(random_generator, n)
    processor = ProcessRequest(random_generator, p)
    model = Model(generator, processor)
    result = model.event_principle()
    print("\nСобытийный принцип\n")
    print(f"Обработанные заявки: {result['Processed requests']}")
    print(f"Повторно обработанные заявки: {result['Reenters requests']}")
    print(f"Длина очереди: {result['Max queue']}")
    print(f"Время обработки: {result['Processed time']}")
