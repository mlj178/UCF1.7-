using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class AnimationHud : MonoBehaviour
{
	[Serializable]
	public struct Anim
	{
		public string name;

		public Sprite[] sprites;

		public Texture[] textures;

		public float[] interval;

		public bool loop;
	}

	[SerializeField]
	private Anim[] animations;

	[SerializeField]
	private Image image;

	[SerializeField]
	private RawImage rawImage;

	public SubscribeableProperty<bool> isPlaying { get; private set; }

	public void Play(int index)
	{
	}

	private void OnDisable()
	{
	}

	public void Play(string animName)
	{
	}

	private IEnumerator AnimationCoroutine(int animID)
	{
		return null;
	}

	public void Stop()
	{
	}
}
