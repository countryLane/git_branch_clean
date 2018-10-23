#!/usr/bin/env python
#coding:utf-8

import sys, os, re, datetime, time
import matplotlib.pyplot as plt
from subprocess import check_output


def getBranchName(branchInfo):
    branchInfoArray = branchInfo.split(' ')
    if len(branchInfoArray) == 2:
        return branchInfoArray[1]
    else:
        return ''


def getBranchCommitterDate(branchInfo):
    branchInfoArray = branchInfo.split(' ')
    if len(branchInfoArray) == 2:
        return datetime.datetime.strptime(branchInfoArray[0], '%Y-%m-%d').date()
    else:
        return ''


def remoteBranches():
    repoPath = sys.argv[1]
    os.chdir(repoPath)
    branches = check_output([
        'git',
        'for-each-ref',
        '--sort=committerdate',
        '--format=\'%(committerdate:short) %(refname:short)\'',
        'refs/remotes/origin'
    ]).split('\n')

    for index in range(len(branches)):
        branches[index] = branches[index].strip('\'')

    return branches


def filterDeletableBranches(allRemoteBranches):
    deletableBranches = []
    for index in range(len(allRemoteBranches)):
        branchInfo = allRemoteBranches[index]
        branchName = getBranchName(branchInfo)
        if branchName.startswith('origin/release') or branchName.startswith('origin/master'):
            continue
        elif len(branchName) == 0:
            continue
        else:
            deletableBranches.append(branchInfo)
    return deletableBranches


def filterOldDeletableBranches(deletableBranches):
    dateStr = sys.argv[2]
    date = datetime.datetime.strptime(dateStr, '%Y-%m-%d').date()
    
    left = 0
    right = len(deletableBranches) - 1
    middle = 0
    while left < right:
        middle = (left + right) / 2
        middleDate = getBranchCommitterDate(deletableBranches[middle])
        if middleDate < date:
            left = middle + 1
        if middleDate > date:
            right = middle - 1
        else:
            break;

    oldDeletableBranches = deletableBranches[:left]
    return  oldDeletableBranches    


def showDiagram(allRemoteBranches):
    times = []
    countOfTime = []
    currentTime = getBranchCommitterDate(allRemoteBranches[0]).strftime('%Y/%m')
    currentCount = 0

    for index in range(len(allRemoteBranches)):
        time = getBranchCommitterDate(allRemoteBranches[index]).strftime('%Y/%m')
        if time == currentTime:
            currentCount += 1
        else:
            times.append(currentTime)
            countOfTime.append(currentCount)
            currentTime = time
            currentCount = 1
    times.append(currentTime)
    countOfTime.append(currentCount)

    x = range(len(times))
    plt.plot(x, countOfTime, linewidth=1.5)
    plt.xticks(x, times, rotation=30, fontsize=5)
    plt.ylabel(u"branch数量")
    plt.title(u"branch数量变化图")
    plt.grid(True)
    plt.savefig("/Users/wangyi/Desktop/branches.jpg")
    plt.show()


def showIncreaseDiagram(allRemoteBranches):
    times = []
    countOfTime = []
    currentTime = getBranchCommitterDate(allRemoteBranches[0]).strftime('%Y/%m')
    count = 0

    for index in range(len(allRemoteBranches)):
        time = getBranchCommitterDate(allRemoteBranches[index]).strftime('%Y/%m')
        if time == currentTime:
            count = index
            continue
        else:
            times.append(currentTime)
            countOfTime.append(index)
            currentTime = time
    times.append(currentTime)
    countOfTime.append(count)

    x = range(len(times))
    plt.plot(x, countOfTime, linewidth=1.5)
    plt.xticks(x, times, rotation=30, fontsize=7)
    plt.ylabel(u"branch数量")
    plt.title(u"branch数量变化图")
    plt.grid(True)
    plt.savefig("/Users/wangyi/Desktop/branches.jpg")
    plt.show()


if __name__ == '__main__':
    allRemoteBranches = remoteBranches()
    deletableBranches = filterDeletableBranches(allRemoteBranches)
    oldDeletableBranches = filterOldDeletableBranches(deletableBranches)

    showDiagram(deletableBranches)
    # showIncreaseDiagram(deletableBranches)
