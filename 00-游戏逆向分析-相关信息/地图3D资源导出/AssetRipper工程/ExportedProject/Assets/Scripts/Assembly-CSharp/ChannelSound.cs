using System;
using UnityEngine;

public class ChannelSound : MonoBehaviour
{
	private float inTime;

	private float outTime;

	private Func<bool> func;

	[SerializeField]
	private AudioSource source;

	private bool shouldPlay;

	private void Update()
	{
	}

	public void SetFadeDuration(float inTime, float outTime)
	{
	}

	public void SetJudgeFunction(Func<bool> func)
	{
	}

	public AudioSource GetSource()
	{
		return null;
	}
}
