using System;

[Serializable]
public struct PostureFloat
{
	public float standIdle;

	public float crouchIdle;

	public float standRun;

	public float crouchRun;

	public float floating;

	public float Get(ShootPosture posture)
	{
		return 0f;
	}

	public float GetMultiplier(ShootPosture posture)
	{
		return 0f;
	}
}
