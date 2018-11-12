import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random as rnd

# matplotlib.rcParams.update({'font.size': 24})


def running_mean(x, length=5000):
    currentValues = []
    samples = 0

    arr = np.zeros_like(x)

    for val in x:
        if len(currentValues) > length:
            currentValues.pop(0)

        currentValues.append(val)
        arr[samples] = np.sum(currentValues) / len(currentValues)
        samples += 1
    return arr


def runForParticleCount(
    particleCount,
    bins=5
):
    # Seed the random generator
    # rnd.seed()

    simulationCount = 500000
    numberOfSteps = 5000

    def runSimulation(doPlot=False):
        stepIndices = []
        stepParticlesInLeft = []
        stepParticlesInRight = []

        # Initial number of particles on the left side
        particlesInLeft = particleCount

        for step in range(numberOfSteps):

            if doPlot:
                stepIndices.append(step)
                stepParticlesInLeft.append(particlesInLeft)
                stepParticlesInRight.append(
                    particleCount - particlesInLeft)

            if rnd.random() <= particlesInLeft / particleCount:
                particlesInLeft -= 1
            else:
                particlesInLeft += 1

            if particlesInLeft < 0:
                particlesInLeft = 0
            if particlesInLeft > particleCount:
                particlesInLeft = particleCount

        if doPlot:
            plt.figure()
            plt.xlabel('Time')
            plt.ylabel('Particles')
            plt.title('Simulation 0 ({0} particles)'.format(particleCount))
            plt.plot(stepIndices, stepParticlesInLeft)
            plt.plot(stepIndices, stepParticlesInRight)
            plt.plot([0, numberOfSteps], [
                     particleCount // 2, particleCount // 2], '--')
            plt.figlegend(('Left', 'Right', 'N / 2'))
            plt.savefig(
                "./plots/3_1/{0}_study.png".format(particleCount), dpi=160)

            plt.figure()
            plt.xlabel('Time')
            plt.ylabel('Particles')
            plt.title('Simulation 0 ({0} particles)'.format(particleCount))
            plt.plot(stepIndices, running_mean(stepParticlesInLeft))
            plt.plot(stepIndices, running_mean(stepParticlesInRight))
            plt.plot([0, numberOfSteps], [
                     particleCount // 2, particleCount // 2], '--')
            plt.figlegend(('Left', 'Right', 'N / 2'))
            plt.savefig(
                "./plots/3_1/{0}_study_mean.png".format(particleCount), dpi=160)

        return (particlesInLeft, particleCount - particlesInLeft)

    endSolutionsLeft = []
    endSolutionsRight = []
    for sim in range(simulationCount):
        if sim % 1000 == 0:
            print("{0:.2f}%".format(100 * sim / simulationCount))
        (particlesLeft, particlesRight) = runSimulation(sim == 0)
        endSolutionsLeft.append(particlesLeft)
        endSolutionsRight.append(particlesRight)

    plt.figure()
    plt.title('All simulations ({0} particles)'.format(particleCount))
    plt.xlabel('Particles')
    plt.ylabel('Count')
    n, bins, patches = plt.hist(
        endSolutionsLeft, bins=bins, range=(0, particleCount))

    plot = plt.plot([
        particleCount // 2, particleCount // 2], [0, np.max(n)], '--', label='N / 2')
    plt.figlegend(handles=(plot))
    plt.savefig("./plots/3_1/{0}_histogram.png".format(particleCount), dpi=160)

    print("Completed {0}".format(particleCount))


runForParticleCount(80, bins=21)
runForParticleCount(64, bins=17)
runForParticleCount(8, bins=np.linspace(-0.5, 8.5, 10))
