using UnityEngine;

public class RecyclableSound : RecyclableObject
{
	public AudioSource audioSource;

	public override void Recycle(bool roundRecycle)
	{
	}

	public void Set3dData(AudioClip clip, Vector2 distance)
	{
	}

	public void Set3dDistance(Vector2 distance)
	{
	}

	public void Set3dDistance(float min, float max)
	{
	}

	public void SetClip(AudioClip clip)
	{
	}

	public void Set2dData(AudioClip clip)
	{
	}
}
